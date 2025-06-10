const path = require('path');
const cors = require('cors');
const express = require('express');

const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const upload = multer({ dest: 'uploads/' });

function setupExpress(app) {
    app.use(cors());
    app.options('*', cors());  // Adjust according to your frontend's origin
    app.use(express.json());



    app.post('/api/upload', upload.single('file'), async (req, res) => {
        const form = new FormData();
        form.append('file', fs.createReadStream(req.file.path), req.file.originalname);

        try {
            const response = await axios.post('http://localhost:8000/upload', form, {
                headers: form.getHeaders(),
            });
            res.send(response.data);
        } catch (err) {
            res.status(500).send(err.message);
        }
    });

    app.post('/api/upload-directory', upload.array('files'), async (req, res) => {
        const form = new FormData();
        req.files.forEach(file => {
            form.append('files', fs.createReadStream(file.path), file.originalname);
        });

        try {
            const response = await axios.post('http://localhost:8000/upload_dir', form, {
                headers: form.getHeaders(),
            });
            res.send(response.data);
        } catch (err) {
            res.status(500).send(err.message);
        }
    });

    app.get('/api/search', async (req, res) => {
        try {
            const response = await axios.get('http://localhost:8000/search', {
                params: { query: req.query.query }
            });
            res.send(response.data);
        } catch (err) {
            res.status(500).send(err.message);
        }
    });


    app.get('/api/ping', (_, res) => res.send('pong'));

    // launch server in production mode
    if (process.env.NODE_ENV === 'production') {
        // Serve production assets
        app.use(express.static('./frontend/dist'))
        // Express will serve up the index.html file
        const filepath = path.join(__dirname, './frontend/dist/index.html');
        app.get('/', (req, res) => {
            res.sendFile(filepath, function (err) {
                if (err)
                    return res.status(err.status).end();
                else
                    return res.status(200).end();
            })
        })
    }
}

module.exports = { setupExpress };