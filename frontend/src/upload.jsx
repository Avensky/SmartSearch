import React, { useState } from 'react';
import axios from 'axios';

export default function Upload({ onUploadComplete }) {
    const [status, setStatus] = useState('');

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file || file.type !== 'application/pdf') {
            setStatus('Please select a valid PDF file.');
            return;
        }

        setStatus('Uploading...');
        const formData = new FormData();
        formData.append('file', file);

        try {
            await axios.post('http://localhost:5001/api/upload', formData);
            setStatus('Upload successful ✅');
            if (onUploadComplete) onUploadComplete();
        } catch (err) {
            setStatus(`Upload failed: ${err.message}`);
        }
    };

    return (
        <div className='button'>
            <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
            />
            <p style={{ margin: 0, fontSize: '0.9em' }}>{status}</p>
        </div>
    );
}
