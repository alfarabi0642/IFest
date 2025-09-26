
function Card({nama_perusahaan="Guest"}){
    return(
        <div className="mt-10 ml-6 font-poppins">
            <img src="src\assets\react.svg" alt="Logo Perusahaan"></img> 
            <h1>{nama_perusahaan}</h1>
            <p>Lorem Ipsum dolor sit amet</p>   
        </div>
    );
}

export default Card