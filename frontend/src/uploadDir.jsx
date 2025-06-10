import React, { useState } from 'react';
import axios from 'axios';

export default function UploadDirectory() {
    const [message, setMessage] = useState('');

    const handleFileChange = async (e) => {
        const selectedFiles = e.target.files;
        if (!selectedFiles || selectedFiles.length === 0) {
            setMessage('No files selected.');
            return;
        }

        const files = Array.from(selectedFiles);
        const formData = new FormData();
        files.forEach((file) => formData.append('files', file));

        try {
            const res = await axios.post('http://localhost:5001/api/upload-directory', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setMessage(res.data.detail || 'Upload successful!');
        } catch (err) {
            setMessage(err.response?.data?.detail || 'Upload failed.');
        }
    };

    return (
        <div className='button'>
            <input
                type="file"
                webkitdirectory="true"
                directory="true"
                multiple
                onChange={handleFileChange}
            />
            <p style={{ margin: 0, fontSize: '0.9em' }}>{message}</p>
        </div>
    );
}
