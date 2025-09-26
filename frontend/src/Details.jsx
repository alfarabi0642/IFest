import defaultLogo from "./assets/googleicon.png";

function Details( {logo=defaultLogo, 
                    judul_kontrak="Development Partnership", 
                    perihal_kontrak="Mobile App Hackathon", 
                    nama_perusahaan="PT Innovatech Indonesia, Bandung"
                } ) {
    return (
        <div className="bg-white right-0 top-0 h-screen w-[58vh] flex flex-col p-7 overflow-y-auto fixed shadow-xl" >
            <div className="text-center">
                <img src={logo} alt="Logo Perusahaan" className="w-20 h-20 rounded-full mx-auto mb-4"></img>
                <h1 className="p-2 font-poppinsbold text-xl text-primary">{judul_kontrak} - {perihal_kontrak}</h1>
                <h2 className="font-poppins text-md mt-2">{nama_perusahaan}</h2>
                <hr className="my-5 border-1"/>
            </div>
            <div>
                <h3 className="text-lg font-poppins font-bold">Contract Overview:</h3>
                <p className="mt-2 ml-4 text-sm font-poppins text-gray-500">Lorem ipsum dolor sit amet</p>
                <h3 className="text-lg mt-6 font-poppins font-bold ">Key Terms:</h3>
                <ul className="font-poppins text-sm list-disc pl-7 leading-9 text-gray-500">
                    <li>Term 1: Description</li>
                    <li>Term 2: Description</li>
                    <li>Term 3: Description</li>
                </ul>
                <h3 className="text-lg mt-6 font-poppins font-bold">Statistics / Metadata:</h3>
                <ul className="font-poppins text-sm list-disc pl-7 leading-9 text-gray-500">
                    <li>Term 1: Description</li>
                    <li>Term 2: Description</li>
                    <li>Term 3: Description</li>
                </ul>
            </div>
            <div className="mt-auto pt-6 text-center flex justify-center items-center">
                <button className="font-poppinsbold bg-gradient-to-r from-secondary to-primary text-white py-2 px-8 rounded-3xl h-13">
                    Download Contract
                </button>
                <button>
                    <img src=""></img>
                </button>
            </div>
        </div>
    );
}

export default Details;