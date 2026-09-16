# Setup interface

React and Tailwind with genuine shadcn/ui New York components from the official registry: https://ui.shadcn.com/r/styles/new-york/{component}.json. Component source and the upstream MIT license are included here.

Run `pnpm install --frozen-lockfile` and `pnpm build` in this directory using Node 22 or newer. The lockfile pins dependencies. The build creates `../assets/setup.html` with all scripts and styles inline. Recipients can open that file directly; they do not need Node, a server or internet access.

Do not edit the generated HTML by hand. Update `src/main.tsx`, `src/fields.ts`, or the component source and rebuild. No personal setup data is stored in this source directory.
