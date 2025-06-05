// stellar-sanctuary.ts
// Stellar Sanctuary (Dark) theme tokens
import { Theme } from '@mui/joy/styles';

const stellarSanctuary: Theme = {
  colorSchemes: {
    dark: {
      palette: {
        primary: {
          solidBg: '#0A0A0A',
          solidColor: '#6B21A8',
        },
        text: {
          primary: '#F3F4F6',
        },
        background: {
          body: 'rgba(107,33,168,0.1)',
        },
      },
    },
  },
  shadows: ['0 0 30px #6B21A8'],
  components: {
    JoySheet: {
      styleOverrides: {
        root: {
          background: 'rgba(107,33,168,0.1)',
          boxShadow: '0 0 30px #6B21A8',
        },
      },
    },
  },
};

export default stellarSanctuary;
