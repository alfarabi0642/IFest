import SearchBar from "../SearchBar.jsx";
import Sort from "../Buttons/Sort.jsx";

function ContractList(){
    return (
        <div className="ml-20 p-6">
            <h1 className="text-2xl font-bold">Contract List</h1>
            <SearchBar/>
            <Sort/>
        </div>
    );
}

export default ContractList