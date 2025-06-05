import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import Upload from './upload';

export default function Search() {
    const [query, setQuery] = useState('');
    const [answer, setAnswer] = useState([]);
    const [type, setType] = useState();
    const [chunks, setChunks] = useState();
    const [status, setStatus] = useState('');
    const textareaRef = useRef();

    const handleSearch = async () => {
        if (!query.trim()) {
            setStatus('Please enter a search query.');
            return;
        }

        try {
            setStatus('Searching...');
            const res = await axios.get('http://localhost:5001/api/search', {
                params: { query },
            });
            const { type, results = [], answer = '' } = res.data || {};

            setType(type);
            setChunks(results);
            setAnswer(answer);


            // setResults(res.data);
            // setResults(Array.isArray(res.data) ? res.data : []);
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
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            boxSizing: 'border-box',
            width: '90%',
            margin: '0 auto'
        }}>
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
                {type === 'chunks' && Array.isArray(chunks) && chunks.map((res, i) => (
                    <li key={i}>
                        <strong>{res.filename}</strong><br />
                        <em>{res.snippet}</em><br />
                        <small>Relevance score: {res.score.toFixed(2)}</small>
                    </li>
                ))}

                {type === 'llm' && (
                    <div style={{ whiteSpace: 'pre-wrap', marginTop: '1em' }}>
                        <strong>AI Answer:</strong><br />
                        {answer}
                    </div>
                )}
            </ul>
        </div>
    );
}
