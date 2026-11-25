import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, sep } from 'node:path'

export const name = 'digital-ic-skills'
export const inject = ['skills']

const names = ['digital-ic-rtl-design', 'digital-ic-verification', 'digital-ic-review-debug', 'digital-ic-amba', 'digital-ic-eda']
const root = new URL('./curriculum/', import.meta.url)

// The repository uses single-line, plain YAML scalars for name and description.
function definition(skill) {
  const path = fileURLToPath(new URL(skill + '/SKILL.md', root))
  const raw = readFileSync(path, 'utf8').replaceAll('\r\n', '\n')
  const header = /^---\n([\s\S]*?)\n---\n/.exec(raw)
  const field = key => header?.[1].split('\n').find(line => line.startsWith(key + ': '))?.slice(key.length + 2).trim()
  if (field('name') !== skill || !field('description')) throw new Error('Invalid skill metadata: ' + path)
  return {
    name: skill, description: field('description'), path, source: 'bundled',
    resourceBase: { kind: 'directory', path: dirname(path).split(sep).join('/') },
    invocation: { modelInvocable: true, userInvocable: true },
    content: raw.slice(header[0].length).trim(),
  }
}

export function apply(ctx) {
  for (const skill of names.map(definition)) ctx.skills.register(skill)
}
