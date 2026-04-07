// Vercel serverless function: exposes the Spotify Client ID for the wave-defect demo.
// Set SPOTIFY_CLIENT_ID in Vercel Environment Variables (same app used by wave2vector-spotify-live).
// The Client ID is safe to expose client-side; PKCE OAuth requires no client secret.
export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store');
  res.json({ spotifyClientId: process.env.SPOTIFY_CLIENT_ID || '' });
}
