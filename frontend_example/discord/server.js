import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';

const app = express();
const PORT = 3000;

app.use(cors());

app.use(express.static('public'));

app.get('/proxy/discord-link', async (req, res) => {
    const jwt = req.headers.authorization;
    const BASE_URL = 'https://api.points.galadriel.com/v1/auth/discord/link';

    try {
        const response = await fetch(BASE_URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': jwt,
            },
            redirect: 'manual'  // Handle redirects manually
        });

        if (response.status === 303) {
            const location = response.headers.get('Location');
            if (location) {
                res.json({ url: location });
            } else {
                res.status(400).json({ error: 'Redirect location not found' });
            }
        } else {
            res.status(response.status).json(await response.json());
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Example at http://localhost:${PORT}`);
});
