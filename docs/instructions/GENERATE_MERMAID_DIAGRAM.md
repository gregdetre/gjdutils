# Generate Mermaid Diagram Images

Quick instructions for creating and updating Mermaid diagrams in your project.

## Setup

Install Mermaid CLI if not already available:
```bash
npm install -g @mermaid-js/mermaid-cli
```

For detailed configuration options, see the [Mermaid CLI documentation](https://github.com/mermaid-js/mermaid-cli).

## File Organization

- **Source files**: Store `.mermaid` files in `docs/diagrams/` (or your preferred documentation directory)
- **Generated files**: Save SVG/PNG outputs in same directory

## File Naming

Mermaid diagrams should follow this naming format: `yyMMdd[letter]_description_in_normal_case.mermaid`

- Generate date prefix with: `date +%y%m%d` (add letter suffix manually if multiple diagrams per day)
- **Alternative**: Use `npx tsx src/ts/cli/sequential-datetime-prefix.ts` for automated sequential prefixes
- Description: lowercase words separated by underscores (except proper names/acronyms)
- Examples:
  - `250701a_flow_iterative_heading_generation.mermaid`
  - `250701b_architecture_glossary_complete.mermaid`
  - `250701c_diagram_tools_flow_ToC.mermaid`

## Generation Commands

**Prefer SVG format** (scalable, web-friendly):
```bash
npx mmdc -i docs/diagrams/FILENAME.mermaid -o docs/diagrams/FILENAME.svg -w 1400 -H 1600 -s 2 -b transparent -t default
```

**PNG only when specifically requested**:
```bash
npx mmdc -i docs/diagrams/FILENAME.mermaid -o docs/diagrams/FILENAME.png -w 1400 -H 1600 -s 2 -b transparent -t default
```

## Best Practices

### Always Regenerate
**Automatically regenerate SVG whenever you update a `.mermaid` file** - keep diagrams in sync with source.

### Simplify Linear Flows
If you have a stack of sequential boxes with no branches, **collapse into a single box** with steps as bullet points:

❌ **Avoid this**:
```mermaid
A[Step 1] --> B[Step 2] --> C[Step 3] --> D[Step 4]
```

✅ **Prefer this**:
```mermaid
Process[Process Flow:<br/>• Step 1<br/>• Step 2<br/>• Step 3<br/>• Step 4]
```

### Syntax Tips
- **Avoid special characters** in node labels (quotes, parentheses)
- **Use emojis** for visual clarity
- **Keep labels concise** - detailed descriptions go in documentation
- **Test syntax** before generating images


### Comments

Include a detailed comment in the `.mermaid` file with a prompt to describe/reproduce this diagram for future reference, including references to relevant files/functions and any other details/intent mentioned by the user. If asked to update the diagram, update the prompt-comment accordingly.


### Spacing

Reduce spacing so that more information fits on the screen.


### Icons

Include icons sparingly, e.g. for different systems, actions, components.


### Fonts

Use `courier` (or other monospaced font) for API endpoints, urls, function names, variables, etc.

Use `italic` or `bold` in other ways to help aid comprehension.


### Use colour

Use colour appropriately to distinguish major components.

For example, you might give different colours to different systems, e.g.
- purple for user
- brown for browser
- orange for mobile/device
- blue for backend
- yellow for database
- purple for cloud storage (including cloud storage services, S3, etc)
- green for payments

Perhaps use one colour scheme for the outer boxes that group things (e.g. for systems), and another colour scheme for inner boxes based on a different typology. Use your judgment.


### Shapes, lines, arrows, etc

For database relationships, use database UML-style lines/arrows/shapes.

Likewise, if there's a domain-standard visual-notational scheme that's relevant for (part of) the diagram, use it there.


## Quick Workflow

1. Generate filename prefix: `date +%y%m%d` (add letter suffix if needed) or `npx tsx src/ts/cli/sequential-datetime-prefix.ts`
2. Create/edit `.mermaid` file with the generated prefix in `docs/diagrams/`
3. Generate SVG: `npx mmdc -i docs/diagrams/FILENAME.mermaid -o docs/diagrams/FILENAME.svg -w 1400 -H 1600 -s 2 -b transparent`
4. Open the SVG in default app: `open docs/diagrams/FILENAME.svg` (or `xdg-open` on Linux)
5. Output the generated filename

### Example Workflow

```bash
# Get the next sequential prefix (manual approach)
date +%y%m%d
# Output: 250701 (add letter suffix manually: 250701a, 250701b, etc.)

# OR get automated sequential prefix
npx tsx src/ts/cli/sequential-datetime-prefix.ts
# Output: 250701a (automatically finds next available letter)

# Create the diagram file
# Create: docs/diagrams/250701d_tool_execution_flow.mermaid

# Generate the SVG
npx mmdc -i docs/diagrams/250701d_tool_execution_flow.mermaid -o docs/diagrams/250701d_tool_execution_flow.svg -w 1400 -H 1600 -s 2 -b transparent

# Open to verify
open docs/diagrams/250701d_tool_execution_flow.svg
```
