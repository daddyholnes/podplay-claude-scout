// SanctuaryLayout.tsx
// Root layout for Podplay Sanctuary, integrating theme, navigation, ThemeSelector, animated background, and Mama Bear
import * as React from 'react';
import { CssVarsProvider } from '@mui/joy/styles';
import Box from '@mui/joy/Box';
import '@fontsource/inter';
import { SanctuaryThemes, getSanctuaryTheme } from '@/themes/SanctuaryTheme';
import Navigation from '@/components/Navigation';
import ThemeSelector from '@/components/ThemeSelector';
import AnimatedSanctuaryBackground from './AnimatedSanctuaryBackground';
import FloatingMamaBear from '@/components/mama-bear/FloatingMamaBear';

export interface SanctuaryLayoutProps {
  children: React.ReactNode;
  themeMode?: 'sky' | 'neon' | 'stellar';
}

export const SanctuaryLayout: React.FC<SanctuaryLayoutProps> = ({ children, themeMode = 'sky' }) => {
  const [mode, setMode] = React.useState<'sky' | 'neon' | 'stellar'>(themeMode);
  const theme = React.useMemo(() => getSanctuaryTheme(mode), [mode]);

  return (
    <CssVarsProvider theme={theme} defaultMode={mode}>
      <Box sx={{ minHeight: '100vh', background: 'var(--sanctuary-surface, #fff)', fontFamily: 'Inter, sans-serif', position: 'relative' }}>
        <AnimatedSanctuaryBackground themeMode={mode} />
        <Box sx={{ position: 'absolute', top: 0, left: 0, width: '100%', zIndex: 2 }}>
          <Navigation onThemeChange={setMode} currentTheme={mode} />
          <ThemeSelector currentTheme={mode} onThemeChange={setMode} />
        </Box>
        <main style={{ position: 'relative', zIndex: 3 }}>{children}</main>
        <FloatingMamaBear mood="attentive" />
      </Box>
    </CssVarsProvider>
  );
};

export default SanctuaryLayout;
