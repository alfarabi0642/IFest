// src/Pages/ContractList.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Import your existing components
import SearchBar from "../SearchBar.jsx";
import Sort from "../Buttons/Sort.jsx";
import Filters from "../Buttons/Filters.jsx";
import Card from "../Card.jsx";
import Add from "../Buttons/Add.jsx";
import Details from '../Details.jsx';

const API_URL = 'http://127.0.0.1:8000';

function ContractList() {
    // --- STATE MANAGEMENT ---
    const [contracts, setContracts] = useState([]); // Initial full list from API
    const [contractsToDisplay, setContractsToDisplay] = useState([]); // The list currently shown on screen
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedContractId, setSelectedContractId] = useState(null);

    // --- DATA FETCHING ---
    useEffect(() => {
        const fetchContracts = async () => {
            try {
                setLoading(true);
                const response = await axios.get(`${API_URL}/contracts`);
                setContracts(response.data);
                setContractsToDisplay(response.data); // Initially, display all contracts
                setError(null);
            } catch (err) {
                setError('Failed to load initial contracts.');
            } finally {
                setLoading(false);
            }
        };
        fetchContracts();
    }, []);

    // --- EVENT HANDLERS ---
    const handleSearch = async () => {
        if (!searchTerm.trim()) {
            setContractsToDisplay(contracts); // If search is cleared, show the original full list
            return;
        }
        try {
            setLoading(true); // Show loading indicator for search
            const response = await axios.get(`${API_URL}/contracts/search`, { params: { q: searchTerm } });
            setContractsToDisplay(response.data || []); // Update display list with search results
            setError(null);
        } catch (err) {
            setError('Search failed.');
        } finally {
            setLoading(false);
        }
    };
    
    const handleCardClick = (documentId) => setSelectedContractId(documentId);
    const handleCloseDetails = () => setSelectedContractId(null);

    // --- RENDER LOGIC ---
    if (error) return <div className="p-6 text-red-600">{error}</div>;

    return (
        <div className="mt-5 ml-53 p-6 relative flex">
            <div className="flex-grow">
                <h1 className="text-2xl font-bold">Contract List</h1>
                <SearchBar 
                    searchTerm={searchTerm}
                    onSearchChange={(e) => setSearchTerm(e.target.value)}
                    onSearchSubmit={handleSearch}
                />
                <Filters />
                <div className="flex justify-between">
                    <Sort />
                    <Add />
                </div>

                <div className="mt-4">
                    {loading ? (
                        <p>Loading...</p>
                    ) : (
                        contractsToDisplay.length > 0 ? (
                            contractsToDisplay.map(contract => (
                                <Card
                                    key={contract.documentId}
                                    judul_kontrak={contract.analysis?.contractMetadata?.documentTitle}
                                    kategori={contract.analysis?.contractMetadata?.documentType}
                                    nama_perusahaan={contract.analysis?.contractSummarization?.parties[0]?.name}
                                    perihal_kontrak={contract.analysis?.contractSummarization?.executiveSummary}
                                    lokasi={contract.analysis?.contractSummarization?.contractLocation}
                                    status={contract.analysis?.contractSummarization?.contractStatus}
                                    periode={contract.analysis?.contractSummarization?.contractPeriod}
                                    value={contract.analysis?.contractSummarization?.contractValue}
                                    onCardClick={() => handleCardClick(contract.documentId)}
                                />
                            ))
                        ) : (
                            <p>No contracts found.</p>
                        )
                    )}
                </div>
            </div>

            {selectedContractId && (
                <Details 
                    documentId={selectedContractId} 
                    onClose={handleCloseDetails} 
                />
            )}
        </div>
    );
}

export default ContractList;