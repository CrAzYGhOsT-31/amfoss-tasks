const key = "38ea76af8b7664e1ff8cf5a2ae5a0c96";  
const cityForm = document.getElementById("cityform");  
const errorImage = document.getElementById("errorImage")
cityForm.addEventListener("submit", wtherSearch);  

function wtherSearch(event) {  
    event.preventDefault();  
    const city = document.getElementById("city").value;  
    const URL = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${key}`;
    console.log(`Fetching details for: ${city}`);  

    fetch(URL)  
        .then(response => {   
            if (!response.ok) {   
                throw new Error("City not found");
            }   
            return response.json();   
        })   
        .then(cordData => {     
            errorImage.style.display = "none";
            if (cordData && cordData.main && cordData.weather) {   
                const temp = (cordData.main.temp-273.15).toFixed(2); 
                const temper = document.getElementById("temper");   
                temper.innerHTML = `${temp}`;   

                const clim = cordData.weather[0].main;  
                const climate = document.getElementById("climate");   
                climate.innerHTML = clim;   

                const icon = cordData.weather[0].icon; 
                const iconUrl = `http://openweathermap.org/img/wn/${icon}@2x.png`;   
                const iconElement = document.getElementById("weatherIcon");   
                iconElement.src = iconUrl;
                errorImage.style.display = "none";   
            } else {  
                console.error("Weather data is not available.");  
            }  
        })  
        .catch(error => {   
            console.error("Error fetching weather data:", error);   
            errorImage.style.display = "block";
        });  
}