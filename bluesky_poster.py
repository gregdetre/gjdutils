#!/usr/bin/env python3
"""
Bluesky posting wrapper with app password authentication and session persistence.

Usage:
    python bluesky_poster.py "Your post text here"
    
Or import and use programmatically:
    from bluesky_poster import BlueskyPoster
    poster = BlueskyPoster()
    poster.post('Hello Bluesky!')
"""

import os
import sys
import json
import time
from typing import Optional
from pathlib import Path
from atproto import Client
from atproto.exceptions import AtProtocolError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class BlueskyPoster:
    """Bluesky posting wrapper with session persistence."""
    
    def __init__(self, session_file: Optional[str] = None, verbose: int = 0):
        """
        Initialize the Bluesky poster.
        
        Args:
            session_file: Path to store session data (default: ~/.bluesky_session.json)
            verbose: Verbosity level (0=quiet, 1=show post URL and session info)
        """
        self.session_file = session_file or os.path.expanduser('~/.bluesky_session.json')
        self.verbose = verbose
        self.client = Client()
        self._authenticated = False
        self.session_data = {}
        self._load_session()
    
    def _load_session(self) -> None:
        """Load existing session data from file."""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.session_data = {}
    
    def _save_session(self, session_string: str, handle: str) -> None:
        """Save session data to file."""
        try:
            self.session_data = {
                'session_string': session_string,
                'handle': handle,
                'timestamp': time.time()
            }
            
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
            os.chmod(self.session_file, 0o600)  # Secure permissions
        except IOError as e:
            print(f"Warning: Could not save session data: {e}")
    
    def _try_existing_session(self) -> bool:
        """Try to use existing session from file."""
        session_string = self.session_data.get('session_string')
        handle = self.session_data.get('handle')
        
        if not session_string or not handle:
            return False
        
        try:
            # Try to restore the session
            self.client.login(handle, session_string=session_string)
            self._authenticated = True
            
            # Export and save the potentially refreshed session
            new_session_string = self.client.export_session_string()
            if new_session_string != session_string:
                self._save_session(new_session_string, handle)
            
            return True
        except Exception as e:
            print(f"Session restoration failed, will re-authenticate: {e}")
            return False
    
    def authenticate(self) -> bool:
        """
        Authenticate with Bluesky using app password from environment variables.
        
        Returns:
            bool: True if authentication successful
        """
        # Try existing session first
        if self._try_existing_session():
            print("✅ Restored existing session")
            if self.verbose >= 1:
                print(f"📁 Session file: {self.session_file}")
                print(f"👤 Handle: {self.session_data.get('handle', 'unknown')}")
            return True
        
        # Get credentials from environment
        handle = os.getenv('BLUESKY_HANDLE')
        password = os.getenv('BLUESKY_PASSWORD')
        
        if not handle or not password:
            print("❌ Missing BLUESKY_HANDLE or BLUESKY_PASSWORD in .env file")
            print("Please add these to your .env file:")
            print("BLUESKY_HANDLE=yourhandle.bsky.social")
            print("BLUESKY_PASSWORD=your-app-password")
            return False
        
        try:
            # Login with app password
            self.client.login(handle, password)
            self._authenticated = True
            
            # Save the session for future use
            session_string = self.client.export_session_string()
            self._save_session(session_string, handle)
            
            print("✅ Authentication successful")
            if self.verbose >= 1:
                print(f"📁 Session saved to: {self.session_file}")
                print(f"👤 Handle: {handle}")
            return True
            
        except AtProtocolError as e:
            if 'Invalid identifier or password' in str(e):
                print("❌ Invalid credentials. Make sure you're using an app password, not your main password.")
                print("Generate an app password at: https://bsky.app/settings/app-passwords")
            else:
                print(f"❌ Authentication failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def post(self, text: str) -> Optional[str]:
        """
        Post text to Bluesky.
        
        Args:
            text: The text content to post
            
        Returns:
            Optional[str]: Post URI if successful, None if failed
        """
        if not self._authenticated:
            if not self.authenticate():
                return None
        
        try:
            response = self.client.send_post(text)
            
            # Try to save refreshed session if tokens were updated
            try:
                session_string = self.client.export_session_string()
                handle = self.session_data.get('handle') or os.getenv('BLUESKY_HANDLE')
                if session_string and handle:
                    self._save_session(session_string, handle)
            except:
                pass  # Session save is optional, don't fail the post
            
            if self.verbose >= 1 and response.uri:
                # Convert AT URI to web URL
                handle = self.session_data.get('handle') or os.getenv('BLUESKY_HANDLE')
                post_id = response.uri.split('/')[-1]
                web_url = f"https://bsky.app/profile/{handle}/post/{post_id}"
                print(f"🔗 Post URL: {web_url}")
            
            return response.uri
        except Exception as e:
            print(f"Failed to post: {e}")
            
            # Try to re-authenticate once if it failed
            if "Invalid token" in str(e) or "ExpiredToken" in str(e):
                print("Session expired, re-authenticating...")
                self._authenticated = False
                if self.authenticate():
                    try:
                        response = self.client.send_post(text)
                        return response.uri
                    except Exception as e2:
                        print(f"Failed to post after re-authentication: {e2}")
            
            return None
    
    def post_with_link(self, text: str, link_url: str, link_title: str = "") -> Optional[str]:
        """
        Post text with an embedded link.
        
        Args:
            text: The text content to post
            link_url: URL to embed
            link_title: Optional title for the link
            
        Returns:
            Optional[str]: Post URI if successful, None if failed
        """
        if not self._authenticated:
            if not self.authenticate():
                return None
        
        try:
            # Create embed for the link
            embed = {
                '$type': 'app.bsky.embed.external',
                'external': {
                    'uri': link_url,
                    'title': link_title or link_url,
                    'description': ''
                }
            }
            
            response = self.client.send_post(text, embed=embed)
            
            # Try to save refreshed session
            try:
                session_string = self.client.export_session_string()
                handle = self.session_data.get('handle') or os.getenv('BLUESKY_HANDLE')
                if session_string and handle:
                    self._save_session(session_string, handle)
            except:
                pass
            
            return response.uri
        except Exception as e:
            print(f"Failed to post with link: {e}")
            return None


def main():
    """Command line interface for posting to Bluesky."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Post to Bluesky')
    parser.add_argument('text', help='The text to post')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Increase verbosity (use -v for verbose output)')
    
    args = parser.parse_args()
    
    poster = BlueskyPoster(verbose=args.verbose)
    
    if not poster.authenticate():
        print("❌ Authentication failed")
        sys.exit(1)
    
    post_uri = poster.post(args.text)
    
    if post_uri:
        print(f"✅ Posted successfully!")
        if args.verbose == 0:  # Only show URI if not verbose (verbose shows web URL)
            print(f"Post URI: {post_uri}")
    else:
        print("❌ Failed to post")
        sys.exit(1)


if __name__ == '__main__':
    main()