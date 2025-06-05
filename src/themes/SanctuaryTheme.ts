// SanctuaryTheme.ts
// Central theme system for Podplay Sanctuary (Sky, Neon, Stellar)
import { extendTheme } from '@mui/joy/styles';
import skySanctuary from './sky-sanctuary';
import neonSanctuary from './neon-sanctuary';
import stellarSanctuary from './stellar-sanctuary';

export const SanctuaryThemes = {
  sky: skySanctuary,
  neon: neonSanctuary,
  stellar: stellarSanctuary,
};

export function getSanctuaryTheme(mode: 'sky' | 'neon' | 'stellar') {
  return extendTheme(SanctuaryThemes[mode]);
}
