import * as React from 'react';
import { useState } from 'react';
import Sheet from '@mui/joy/Sheet';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';
import Input from '@mui/joy/Input';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import Checkbox from '@mui/joy/Checkbox';
import Slider from '@mui/joy/Slider';
import CircularProgress from '@mui/joy/CircularProgress';
import Alert from '@mui/joy/Alert';
import '@fontsource/inter';

interface ScrapeResult {
  stdout: string;
  stderr: string;
  success: boolean;
}

export const Mem0IngestionPanel: React.FC = () => {
  const [url, setUrl] = useState('');
  const [allowed, setAllowed] = useState<string[]>([]);
  const [maxDepth, setMaxDepth] = useState<number>(2);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScrapeResult | null>(null);
  const [siteLinks, setSiteLinks] = useState<string[]>([]);
  const [fetchingLinks, setFetchingLinks] = useState(false);

  // Fetch links from the site for subdir selection
  const fetchLinks = async () => {
    setFetchingLinks(true);
    setSiteLinks([]);
    try {
      const res = await fetch('/api/utils/extract_links', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await res.json();
      setSiteLinks(data.links || []);
    } catch {
      setSiteLinks([]);
    }
    setFetchingLinks(false);
  };

  const handleAllowedChange = (link: string) => {
    setAllowed(prev => prev.includes(link) ? prev.filter(l => l !== link) : [...prev, link]);
  };

  const handleScrape = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('/api/ingest/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, allowed, max_depth: maxDepth })
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setResult({ success: false, stdout: '', stderr: String(e) });
    }
    setLoading(false);
  };

  return (
    <Sheet variant="soft" sx={{ p: 3, borderRadius: 12, boxShadow: 'lg', width: 420, position: 'fixed', right: 32, bottom: 32, zIndex: 1200 }}>
      <Typography level="h4" fontFamily="inter" mb={2}>
        Mem0 Knowledge Ingestion
      </Typography>
      <Input
        placeholder="Enter site URL (https://...)"
        value={url}
        onChange={e => setUrl(e.target.value)}
        fullWidth
        sx={{ mb: 2 }}
      />
      <Button onClick={fetchLinks} disabled={!url || fetchingLinks} size="sm" sx={{ mb: 2 }}>
        {fetchingLinks ? <CircularProgress size="sm" /> : 'Fetch Site Links'}
      </Button>
      {siteLinks.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography level="body2" mb={1}>Select subdirectories to allow:</Typography>
          <List size="sm" sx={{ maxHeight: 120, overflow: 'auto', border: '1px solid #eee', borderRadius: 6 }}>
            {siteLinks.map(link => (
              <ListItem key={link}>
                <Checkbox
                  label={link}
                  checked={allowed.includes(link)}
                  onChange={() => handleAllowedChange(link)}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
      <Box sx={{ mb: 2 }}>
        <Typography level="body2">Max Depth: {maxDepth}</Typography>
        <Slider min={1} max={5} value={maxDepth} onChange={(_, v) => setMaxDepth(Number(v))} sx={{ width: 180 }} />
      </Box>
      <Button
        onClick={handleScrape}
        loading={loading}
        disabled={!url || loading}
        fullWidth
        sx={{ mt: 1 }}
      >
        Scrape & Index to Mem0
      </Button>
      {result && (
        <Alert color={result.success ? 'success' : 'danger'} sx={{ mt: 2 }}>
          {result.success ? 'Success!' : 'Error'}
          <pre style={{ fontSize: 12, whiteSpace: 'pre-wrap', margin: 0 }}>{result.stdout || result.stderr}</pre>
        </Alert>
      )}
    </Sheet>
  );
};

export default Mem0IngestionPanel;
