import SearchBar from "../SearchBar.jsx";
import Sort from "../Buttons/Sort.jsx";
import Add from "../Buttons/Add.jsx";
import Filters from "../Buttons/Filters.jsx";

function ContractList(){
    return (
        <div className="mt-5 ml-53 p-6">
            <h1 className="text-2xl font-bold">Contract List</h1>
            <SearchBar/>
            <Filters/>
            <div className="flex justify-between">
                <Sort/>
                <Add/>
            </div>
            
        </div>
    );
}

export default ContractList