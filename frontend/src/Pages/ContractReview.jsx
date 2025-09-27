import defaultLogo from "../assets/googleicon.png"
import ProgressBar from "../ProgressBar";

function ContractReview({logo=defaultLogo, 
                judul_kontrak="Development Partnership Agreement", 
                perihal_kontrak="Mobile App Hackathon", 
                nama_perusahaan="PT Innovatech Indonesia",
                lokasi="Bandung, Indonesia",
                kategori="Partnership",
                status="Unapproved",
                periode=" 1 Sep - 1 Okt 2025",
                value="IDR 20.000.000"}){
    return(
        <div className=" ml-[14vw] mr-8 p-6 my-5 h-screen flex  justify-center gap-x-5 font-poppins">
            <div className="flex-col flex w-1/3 justify-center "> 
                <div className="flex-col flex justify-center">
                    <img src={logo} alt="Logo Perusahaan" className="w-[7.5vw] h-[7.5vw] mx-auto mt-13 mb-5"></img>
                    <h1 className="mx-auto font-bold text-[1.8vw] p-3 mt-6 bg-gray-300 rounded-3xl">{nama_perusahaan}</h1>
                    <h2 className="mx-auto text-primary text-[1.2vw] pt-2 ">{judul_kontrak}</h2>
                    <p className="ml-7 mt-10 font-semibold text-2xl underline">About</p>
                    <div className="flex-col justify-center items-center p-5 text-lg text-gray-500 ">
                        <div className="l mb-5">
                            <ul className="list-disc mb-3 ml-5 leading-9">
                                <li>Perihal : {perihal_kontrak}</li>
                                <li>Lokasi: {lokasi}</li>
                                <li>Kategori: {kategori}</li>
                            </ul>
                        </div>
                        <div className="">
                            <ul className="list-disc my-b ml-5 leading-9">
                                <li>Status: {status}</li>
                                <li>Periode: {periode}</li>
                                <li>Value: {value} / month</li>
                            </ul>
                        </div>
                    </div>

                </div>
            </div>
            <div className="flex-col w-1/3 text-center">
                <div className="pt-23">
                    <h3 className="text-2xl font-poppins font-bold">Contract Summary:</h3>
                    <p className="mt-2 ml-4 text-lg font-poppins text-gray-500">Lorem ipsum dolor sit amet</p>
                    <h3 className="pt-7 text-2xl mt-6 font-poppins font-bold ">Key Terms:</h3>
                    <ul className="pt-5 font-poppins text-lg list-disc list-inside leading-9 text-gray-500">
                        <li>Term 1: Description</li>
                        <li>Term 2: Description</li>
                        <li>Term 3: Description</li>
                    </ul>
                    <h3 className="pt-7 text-2xl mt-6 font-poppins font-bold">Statistics / Metadata:</h3>
                    <ul className="pt-5 font-poppins text-lg list-disc list-inside leading-9 text-gray-500">
                        <li>Term 1: Description</li>
                        <li>Term 2: Description</li>
                        <li>Term 3: Description</li>
                    </ul>
            </div>  
            </div>
            <div className="flex-col w-1/3 pt-17">
                <p className="pl-18">Test1</p>
                <ProgressBar classsName="hover:scale-102"/>
                <p className="pl-18">Test2</p>
                <ProgressBar/>
                <p className="pl-18">Test3</p>
                <ProgressBar/>
                <p className="pl-18">Test4</p>
                <ProgressBar/>
            </div>
        </div>
    );
}

export default ContractReview   