import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Import your existing components
import SearchBar from "../SearchBar.jsx";
import Sort from "../Buttons/Sort.jsx";
import Filters from "../Buttons/Filters.jsx";
import Card from "../Card.jsx";
import Add from "../Buttons/Add.jsx";

const API_URL = 'http://127.0.0.1:8000'; // Your backend URL

function ContractList() {
    // State to hold the list of contracts, loading status, and any errors
    const [contracts, setContracts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // This useEffect hook will run once when the component is first rendered
    useEffect(() => {
        const fetchContracts = async () => {
            try {
                setLoading(true);
                // The API call to your Python backend's GET /contracts endpoint
                const response = await axios.get(`${API_URL}/contracts`);
                setContracts(response.data); // Store the array of contracts in our state
                setError(null);
            } catch (err) {
                setError('Failed to fetch contracts. Is the backend server running?');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchContracts();
    }, []); // The empty array [] ensures this runs only once

    // --- Conditional Rendering ---
    // Show a loading message while fetching data
    if (loading) {
        return <div className="p-6">Loading contracts...</div>;
    }

    // Show an error message if the API call fails
    if (error) {
        return <div className="p-6" style={{ color: 'red' }}>{error}</div>;
    }

    return (
        <div className="mt-5 ml-53 p-6 relative">
            <h1 className="text-2xl font-bold">Contract List</h1>
            <SearchBar />
            <Filters />
            <div className="flex justify-between ">
                <Sort />
                <Add />
            </div>
            
            {/* --- DYNAMIC CARD LIST --- */}
            {/* We map over the 'contracts' array from our state. */}
            {/* For each 'contract' object in the array, we render one <Card /> component. */}
            {contracts.map(contract => (
                <Card
                    key={contract.documentId}
                    judul_kontrak={contract.analysis.contractMetadata.documentTitle}
                    kategori={contract.analysis.contractMetadata.documentType}
                    // The rest of the props will use the default values from your Card component for now
                />
            ))}
        </div>
    );
}

export default ContractList;