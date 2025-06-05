// neon-sanctuary.ts
// Neon Sanctuary (Purple) theme tokens
import { Theme } from '@mui/joy/styles';

const neonSanctuary: Theme = {
  colorSchemes: {
    dark: {
      palette: {
        primary: {
          solidBg: 'linear-gradient(135deg, #581C87 0%, #BE185D 50%, #1E3A8A 100%)',
          solidColor: '#EC4899',
        },
        text: {
          primary: '#FFFFFF',
        },
        background: {
          body: 'rgba(88,28,135,0.3)',
        },
      },
    },
  },
  shadows: ['0 0 30px rgba(236,72,153,0.4)'],
  components: {
    JoySheet: {
      styleOverrides: {
        root: {
          boxShadow: '0 0 30px rgba(236,72,153,0.4)',
          border: '1px solid #EC4899',
        },
      },
    },
  },
};

export default neonSanctuary;
