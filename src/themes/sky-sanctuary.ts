// sky-sanctuary.ts
// Sky Sanctuary (Light) theme tokens
import { Theme } from '@mui/joy/styles';

const skySanctuary: Theme = {
  colorSchemes: {
    light: {
      palette: {
        primary: {
          solidBg: 'linear-gradient(135deg, #E0F2FE 0%, #DBEAFE 100%)',
          solidColor: '#0EA5E9',
        },
        text: {
          primary: '#1E40AF',
        },
        background: {
          body: 'rgba(255,255,255,0.8)',
        },
      },
    },
  },
  shadows: ['0 8px 32px rgba(14, 165, 233, 0.15)'],
  components: {
    JoySheet: {
      styleOverrides: {
        root: {
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(255,255,255,0.2)',
          boxShadow: '0 8px 32px rgba(14,165,233,0.15)',
        },
      },
    },
  },
};

export default skySanctuary;
