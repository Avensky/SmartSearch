import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import Upload from './upload';

export default function Search() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [status, setStatus] = useState('');
    const textareaRef = useRef();

    const handleSearch = async () => {
        if (!query.trim()) {
            setStatus('Please enter a search query.');
            return;
        }

        try {
            setStatus('Searching...');
            const res = await axios.get('http://localhost:3001/api/search', {
                params: { query },
            });
            setResults(res.data);
            setStatus(res.data.length ? '' : 'No results found.');
        } catch (err) {
            setStatus(`Search failed: ${err.message}`);
        }
    };

    const handleInput = (e) => {
        setQuery(e.target.value);
        autoGrow();
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSearch();
        }
    };

    const autoGrow = () => {
        const el = textareaRef.current;
        el.style.height = 'auto';
        el.style.height = `${el.scrollHeight}px`;
    };

    useEffect(() => {
        autoGrow();
    }, []);

    return (
        <div style={{ width: '100%', boxSizing: 'border-box' }}>
            <textarea
                ref={textareaRef}
                placeholder="Ask anything"
                value={query}
                onChange={handleInput}
                onKeyDown={handleKeyDown}
                rows={1}
                style={{
                    width: '100%',
                    padding: '8px',
                    resize: 'none',
                    overflow: 'hidden',
                    lineHeight: '1.5',
                }}
            />
            <div className='bar'>
                <Upload />
                <button
                    className='button'
                    onClick={handleSearch}
                    style={{ display: 'block' }}>
                    Search
                </button>
            </div>
            <p>{status}</p>
            <ul>
                {results.map((res, i) => (
                    <li key={i} style={{ marginBottom: '1em' }}>
                        <strong>{res.filename}</strong><br />
                        <em>{res.snippet}...</em><br />
                        <small>Relevance: {res.score.toFixed(2)}</small>
                    </li>
                ))}
            </ul>
        </div>
    );
}
