document.addEventListener('DOMContentLoaded', function() {
    const tabs = ['Nutech_Tab', 'Margalla_Tab', 'Graphs_Tab', 'Data_Tab'];
    const buttons = ['Nutech_Button', 'Margalla_Button', 'Graphs_Button', 'Data_Button'];
    let currentTab = 0;
    let intervalActive = false; // To track if the interval is active for specific tabs
    
    function showTab(index) {
        // Hide all content sections
        tabs.forEach(tab => document.getElementById(tab).classList.add('hidden_content'));
        // Show the selected content section
        document.getElementById(tabs[index]).classList.remove('hidden_content');
    
        // Update button styles
        buttons.forEach((btn, i) => {
            const button = document.getElementById(btn);
            if (i === index) {
                button.classList.add('button_active');
                button.classList.remove('button_inactive');
            } else {
                button.classList.remove('button_active');
                button.classList.add('button_inactive');
            }
        });
    
        // Manage interval activation based on the tab
        if (tabs[index] === 'Nutech_Tab' || tabs[index] === 'Margalla_Tab') {
            if (!intervalActive) {
                intervalActive = true;
                startInterval();
            }
        } else {
            if (intervalActive) {
                intervalActive = false;
                clearInterval(tabSwitchInterval);
            }
        }
    }
    
    let tabSwitchInterval; // Variable to store the interval ID
    
    function startInterval() {
        tabSwitchInterval = setInterval(() => {
            // Switch to the next tab only if it's Nutech_Tab or Margalla_Tab
            if (currentTab === 0 || currentTab === 1) {
                currentTab = (currentTab + 1) % 2; // Only switch between Nutech_Tab and Margalla_Tab
                showTab(currentTab);
            }
        }, 30000);
    }
    
    showTab(currentTab);
    
    buttons.forEach((btn, index) => {
        document.getElementById(btn).addEventListener('click', () => {
            currentTab = index;
            showTab(currentTab);
        });
    });

    const graphTabs = ['Daily_Graphs_Tab', 'Weekly_Graphs_Tab', 'Monthly_Graphs_Tab'];
    const graphButtons = ['Graphs_Daily_Button', 'Graphs_Weekly_Button', 'Graphs_Monthly_Button'];
    let currentGraphTab = 0;

    function showGraphTab(index) {
        // Hide all content sections
        graphTabs.forEach(tab => document.getElementById(tab).classList.add('graph_hidden_content'));
        // Show the selected content section
        document.getElementById(graphTabs[index]).classList.remove('graph_hidden_content');

        // Update button styles
        graphButtons.forEach((btn, i) => {
            const button = document.getElementById(btn);
            if (i === index) {
                button.classList.add('graph_button_active');
                button.classList.remove('graph_button_inactive');
            } else {
                button.classList.remove('graph_button_active');
                button.classList.add('graph_button_inactive');
            }
        });
    }
    showGraphTab(currentGraphTab);
    graphButtons.forEach((btn, index) => {
        document.getElementById(btn).addEventListener('click', () => {
            currentGraphTab = index;
            showGraphTab(currentGraphTab);
        });
    });

    const rows = document.querySelectorAll('#weatherData tr');

    rows.forEach(row => {
        const tempCell = row.cells[2];
        const pressureCell = row.cells[3];
        const windSpeedCell = row.cells[4];
        const windDirectionCell = row.cells[5];
        const humidityCell = row.cells[6];
        const rainCell = row.cells[7];
        const solarCell = row.cells[8];
        const soilMoistureCell = row.cells[9];
        const evapotranspirationCell = row.cells[10];
        const co2Cell = row.cells[11];
        const opticalParticlesCell = row.cells[12];
        const pollenCell = row.cells[13];

        const temp = parseInt(tempCell.textContent);
        const rain = parseFloat(rainCell.textContent);
        const humidity = parseInt(humidityCell.textContent);
        const windSpeed = parseInt(windSpeedCell.textContent);
        const windDirection = windDirectionCell.textContent;
        const pressure = parseInt(pressureCell.textContent);
        const evapotranspiration = parseFloat(evapotranspirationCell.textContent);
        const co2 = parseInt(co2Cell.textContent);
        const opticalParticles = parseFloat(opticalParticlesCell.textContent);
        const solar = parseInt(solarCell.textContent);
        const soilMoisture = parseInt(soilMoistureCell.textContent);
        const pollen = parseInt(pollenCell.textContent);

        if (evapotranspiration>=15){
            evapotranspirationCell.style.backgroundColor = '#757575';
        } else if (evapotranspiration==14) {
            evapotranspirationCell.style.backgroundColor = '#7A7A7A';
        } else if (evapotranspiration==13) {
            evapotranspirationCell.style.backgroundColor = '#808080';
        } else if (evapotranspiration==12) {
            evapotranspirationCell.style.backgroundColor = '#858585';
        } else if (evapotranspiration==11) {
            evapotranspirationCell.style.backgroundColor = '#8A8A8A';
        } else if (evapotranspiration==10) {
            evapotranspirationCell.style.backgroundColor = '#8F8F8F';
        } else if (evapotranspiration==9) {
            evapotranspirationCell.style.backgroundColor = '#949494';
        } else if (evapotranspiration==8) {
            evapotranspirationCell.style.backgroundColor = '#999999';
        } else if (evapotranspiration==7) {
            evapotranspirationCell.style.backgroundColor = '#9E9E9E';
        } else if (evapotranspiration==6) {
            evapotranspirationCell.style.backgroundColor = '#A3A3A3';
        } else if (evapotranspiration==5) {
            evapotranspirationCell.style.backgroundColor = '#A8A8A8';
        } else if (evapotranspiration==4) {
            evapotranspirationCell.style.backgroundColor = '#ADADAD';
        } else if (evapotranspiration==3) {
            evapotranspirationCell.style.backgroundColor = '#B3B3B3';
        } else if (evapotranspiration==2) {
            evapotranspirationCell.style.backgroundColor = '#B8B8B8';
        } else if (evapotranspiration==1) {
            evapotranspirationCell.style.backgroundColor = '#BDBDBD';
        } else {
            evapotranspirationCell.style.backgroundColor = '#C2C2C2';
        }


        if (pollen>=1500) {
            pollenCell.style.backgroundColor = '#47126b'; // Dark purple - High pollen
        } else if (pollen>=1400) {
            pollenCell.style.backgroundColor = '#FF9500'; // Interpolate between high and moderate
        } else if (pollen>=1300) {
            pollenCell.style.backgroundColor = '#FF990A'; // Interpolate between high and moderate
        } else if (pollen>=1200) {
            pollenCell.style.backgroundColor = '#FF9D14'; // Interpolate between high and moderate
        } else if (pollen>=1100) {
            pollenCell.style.backgroundColor = '#FFA21F'; // Interpolate between high and moderate
        } else if (pollen>=1000) {
            pollenCell.style.backgroundColor = '#FFA629'; // Moderate pollen - Light purple
        } else if (pollen>=900) {
            pollenCell.style.backgroundColor = '#FFAA33'; // Interpolate between moderate and low
        } else if (pollen>=800) {
            pollenCell.style.backgroundColor = '#FFAE3D'; // Interpolate between moderate and low
        } else if (pollen>=700) {
            pollenCell.style.backgroundColor = '#FFB347'; // Interpolate between moderate and low
        } else if (pollen>=600) {
            pollenCell.style.backgroundColor = '#FFB752'; // Interpolate between moderate and low
        } else if (pollen>=500) {
            pollenCell.style.backgroundColor = '#FFBB5C'; // Interpolate between moderate and low
        } else if (pollen>=400) {
            pollenCell.style.backgroundColor = '#FFBF66'; // Interpolate between moderate and low
        } else if (pollen>=300) {
            pollenCell.style.backgroundColor = '#FFC370'; // Interpolate between moderate and low
        } else if (pollen>=200) {
            pollenCell.style.backgroundColor = '#FFC87A'; // Interpolate between moderate and low
        } else if (pollen>=100) {
            pollenCell.style.backgroundColor = '#FFCC85'; // Interpolate between moderate and low
        } else {
            pollenCell.style.backgroundColor = '#FFD08F'; // White - Low pollen
        }

        if (co2 >= 4500) {
            co2Cell.style.backgroundColor = '#036666'; // Interpolate between high and moderate
        } else if (co2 >= 4000) {
            co2Cell.style.backgroundColor = '#14746f'; // Interpolate between high and moderate
        } else if (co2 >= 3500) {
            co2Cell.style.backgroundColor = '#248277'; // Interpolate between high and moderate
        } else if (co2 >= 3000) {
            co2Cell.style.backgroundColor = '#358f80'; // Interpolate between high and moderate
        } else if (co2 >= 2500) {
            co2Cell.style.backgroundColor = '#469d89'; // Moderate CO2 - Light purple
        } else if (co2 >= 2000) {
            co2Cell.style.backgroundColor = '#56ab91'; // Interpolate between moderate and low
        } else if (co2 >= 1500) {
            co2Cell.style.backgroundColor = '#67b99a'; // Interpolate between moderate and low
        } else if (co2 >= 1000) {
            co2Cell.style.backgroundColor = '#78c6a3'; // Interpolate between moderate and low
        } else if (co2 >= 500) {
            co2Cell.style.backgroundColor = '#88d4ab'; // Interpolate between moderate and low
        } else {
            co2Cell.style.backgroundColor = '#99e2b4'; // Interpolate between moderate and low
        }

        if (opticalParticles >= 100) {
            opticalParticlesCell.style.backgroundColor = '#656d4a';
        } else if (opticalParticles >= 90) {
            opticalParticlesCell.style.backgroundColor = '#606f49';
        } else if (opticalParticles >= 80) {
            opticalParticlesCell.style.backgroundColor = '#728359';
        } else if (opticalParticles >= 70) {
            opticalParticlesCell.style.backgroundColor = '#849669';
        } else if (opticalParticles >= 60) {
            opticalParticlesCell.style.backgroundColor = '#97a97c';
        } else if (opticalParticles >= 50) {
            opticalParticlesCell.style.backgroundColor = '#a6b98b';
        } else if (opticalParticles >= 40) {
            opticalParticlesCell.style.backgroundColor = '#b5c99a';
        } else if (opticalParticles >= 30) {
            opticalParticlesCell.style.backgroundColor = '#c2d5aa';
        } else if (opticalParticles >= 20) {
            opticalParticlesCell.style.backgroundColor = '#cfe1b9';
        } else if (opticalParticles >= 10) {
            opticalParticlesCell.style.backgroundColor = '#dcebca';
        } else {
            opticalParticlesCell.style.backgroundColor = '#e9f5db';
        }
        
        if (windSpeed >=200) {
            windSpeedCell.style.backgroundColor = '#774936'; // Royal blue - High wind speed
        } else if (windSpeed >=180) {
            windSpeedCell.style.backgroundColor = '#8a5a44'; // Interpolate between high and moderate
        } else if (windSpeed >=160) {
            windSpeedCell.style.backgroundColor = '#9d6b53'; // Interpolate between high and moderate
        } else if (windSpeed >=140) {
            windSpeedCell.style.backgroundColor = '#b07d62'; // Interpolate between high and moderate
        } else if (windSpeed >=120) {
            windSpeedCell.style.backgroundColor = '#c38e70'; // Interpolate between high and moderate
        } else if (windSpeed >=100) {
            windSpeedCell.style.backgroundColor = '#cd9777'; // Interpolate between high and moderate
        } else if (windSpeed >=80) {
            windSpeedCell.style.backgroundColor = '#d69f7e'; // Interpolate between high and moderate
        } else if (windSpeed >=60) {
            windSpeedCell.style.backgroundColor = '#deab90'; // Interpolate between high and moderate
        } else if (windSpeed >=40) {
            windSpeedCell.style.backgroundColor = '#e6b8a2'; // Interpolate between high and moderate
        } else if (windSpeed >=20) {
            windSpeedCell.style.backgroundColor = '#edc4b3'; // Interpolate between high and moderate
        } else {
            windSpeedCell.style.backgroundColor = '#ede0d4'; // Interpolate between high and moderate
        }


        if (humidity >= 100) {
        humidityCell.style.backgroundColor = '#47126b'; // Blue - High humidity
        } else if (humidity >= 90) {
        humidityCell.style.backgroundColor = '#571089'; // Interpolate between high and moderate
        } else if (humidity >= 80) {
        humidityCell.style.backgroundColor = '#6411ad'; // Interpolate between high and moderate
        } else if (humidity >= 70) {
        humidityCell.style.backgroundColor = '#6d23b6'; // Interpolate between high and moderate
        } else if (humidity >= 60) {
        humidityCell.style.backgroundColor = '#822faf'; // Interpolate between high and moderate
        } else if (humidity >= 50) {
        humidityCell.style.backgroundColor = '#973aa8'; // Light green - Moderate humidity
        } else if (humidity >= 40) {
        humidityCell.style.backgroundColor = '#ac46a1'; // Interpolate between moderate and low
        } else if (humidity >= 30) {
        humidityCell.style.backgroundColor = '#c05299'; // Interpolate between moderate and low
        } else if (humidity >= 20) {
        humidityCell.style.backgroundColor = '#d55d92'; // Interpolate between moderate and low
        } else if (humidity >= 10) {
        humidityCell.style.backgroundColor = '#ea698b'; // Interpolate between moderate and low
        } else {
        humidityCell.style.backgroundColor = '#ff7aa2'; // Pink - Low humidity
        }

        if (rain >= 200) {
        rainCell.style.backgroundColor = '#072ac8'; // Royal blue - High rainfall
        } else if (rain >= 180) {
        rainCell.style.backgroundColor = '#0d47a1'; // Interpolate between high and moderate
        } else if (rain >= 160) {
        rainCell.style.backgroundColor = '#1565c0'; // Interpolate between high and moderate
        } else if (rain >= 140) {
        rainCell.style.backgroundColor = '#1976d2'; // Interpolate between high and moderate
        } else if (rain >= 120) {
        rainCell.style.backgroundColor = '#1e88e5'; // Interpolate between high and moderate
        } else if (rain >= 100) {
        rainCell.style.backgroundColor = '#2196f3'; // Cyan - Moderate rainfall
        } else if (rain >= 80) {
        rainCell.style.backgroundColor = '#42a5f5'; // Interpolate between moderate and low
        } else if (rain >= 60) {
        rainCell.style.backgroundColor = '#64b5f6'; // Interpolate between moderate and low
        } else if (rain >= 40) {
        rainCell.style.backgroundColor = '#90caf9'; // Interpolate between moderate and low
        } else if (rain >= 20) {
        rainCell.style.backgroundColor = '#bbdefb'; // Interpolate between moderate and low
        } else {
        rainCell.style.backgroundColor = '#e3f2fd'; // Sky blue - Low rainfall
        }


        if (pressure >= 1100) {
        pressureCell.style.backgroundColor = '#47126b'; // Dark purple - High pressure
        } else if (pressure >= 1085) {
        pressureCell.style.backgroundColor = '#571089'; // Interpolate between high and moderate
        } else if (pressure >= 1070) {
        pressureCell.style.backgroundColor = '#6411ad'; // Interpolate between high and moderate
        } else if (pressure >= 1055) {
        pressureCell.style.backgroundColor = '#6d23b6'; // Interpolate between high and moderate
        } else if (pressure >= 1040) {
        pressureCell.style.backgroundColor = '#7b2cbf'; // Interpolate between high and moderate
        } else if (pressure >= 1025) {
        pressureCell.style.backgroundColor = '#6247aa'; // Moderate pressure - Light purple
        } else if (pressure >= 1010) {
        pressureCell.style.backgroundColor = '#7251b5'; // Interpolate between moderate and low
        } else if (pressure >= 995) {
        pressureCell.style.backgroundColor = '#815ac0'; // Interpolate between moderate and low
        } else if (pressure >= 980) {
        pressureCell.style.backgroundColor = '#9163cb'; // Interpolate between moderate and low
        } else if (pressure >= 965) {
        pressureCell.style.backgroundColor = '#a06cd5'; // Interpolate between moderate and low
        } else if (pressure >= 950) {
        pressureCell.style.backgroundColor = '#b185db'; // Interpolate between moderate and low
        } else if (pressure >= 935) {
        pressureCell.style.backgroundColor = '#c19ee0'; // Interpolate between moderate and low
        } else if (pressure >= 920) {
        pressureCell.style.backgroundColor = '#d2b7e5'; // Interpolate between moderate and low
        } else if (pressure >= 905) {
        pressureCell.style.backgroundColor = '#dac3e8'; // Lightest purple - Low pressure
        } else {
        pressureCell.style.backgroundColor = '#dec9e9'; // White 
        }

        if (solar >= 1100) {
        solarCell.style.backgroundColor = '#ff8000'; // High radiation - Bright yellow
        } else if (solar >= 1050) {
        solarCell.style.backgroundColor = '#ff8c00'; // Moderate radiation - Yellow
        } else if (solar >= 1000) {
        solarCell.style.backgroundColor = '#ff9900'; // Moderate radiation - Yellow
        } else if (solar >= 950) {
        solarCell.style.backgroundColor = '#ffa600'; // Moderate radiation - Yellow
        } else if (solar >= 900) {
        solarCell.style.backgroundColor = '#ffb300'; // Moderate radiation - Yellow
        } else if (solar >= 850) {
        solarCell.style.backgroundColor = '#ffbf00'; // Moderate radiation - Yellow
        } else if (solar >= 800) {
        solarCell.style.backgroundColor = '#ffcc00'; // Moderate radiation - Yellow
        } else if (solar >= 750) {
        solarCell.style.backgroundColor = '#ffd900'; // Moderate radiation - Yellow
        } else if (solar >= 700) {
        solarCell.style.backgroundColor = '#ffe600'; // Low radiation - Light yellow
        } else if (solar >= 650) {
        solarCell.style.backgroundColor = '#ffdd1f'; // Interpolate between low and moderate
        } else if (solar >= 600) {
        solarCell.style.backgroundColor = '#ffe433'; // Interpolate between low and moderate
        } else if (solar >= 550) {
        solarCell.style.backgroundColor = '#ffe747'; // Interpolate between low and moderate
        } else if (solar >= 500) {
        solarCell.style.backgroundColor = '#ffec5c'; // Interpolate between low and moderate
        } else if (solar >= 450) {
        solarCell.style.backgroundColor = '#ffee70'; // Interpolate between low and moderate
        } else if (solar >= 400) {
        solarCell.style.backgroundColor = '#fff185'; // Interpolate between low and moderate
        } else if (solar >= 350) {
        solarCell.style.backgroundColor = '#fff599'; // Interpolate between low and moderate
        } else if (solar >= 300) {
        solarCell.style.backgroundColor = '#fff8a5'; // Interpolate between low and moderate
        } else if (solar >= 250) {
        solarCell.style.backgroundColor = '#ffffb7'; // Interpolate between low and moderate
        } else if (solar >= 200) {
        solarCell.style.backgroundColor = '#fff6cc'; // Interpolate between low and moderate
        } else if (solar >= 150) {
        solarCell.style.backgroundColor = '#fffae5'; // Interpolate between low and moderate
        } else {
            solarCell.style.backgroundColor = '#fff9f9'; // White
        }

        if (windDirection == "North") {
            windDirectionCell.style.backgroundColor = '#007bff'; // Blue
        } else if (windDirection == "South") {
            windDirectionCell.style.backgroundColor = '#dc3545'; // Red
        } else if (windDirection == "East") {
            windDirectionCell.style.backgroundColor = '#28a745'; // Green
        } else if (windDirection == "West") {
            windDirectionCell.style.backgroundColor = '#ffc107'; // Yellow
        } else if (windDirection == "NE") {
            windDirectionCell.style.backgroundColor = '#00b050'; // Teal
        } else if (windDirection == "NW") {
            windDirectionCell.style.backgroundColor = '#6f42c0'; // Purple
        } else if (windDirection == "SE") {
            windDirectionCell.style.backgroundColor = '#fd7e14'; // Orange
        } else if (windDirection == "SW") {
            windDirectionCell.style.backgroundColor = '#17a2b8'; // Cyan
        } else if (windDirection == "NNE") {
            windDirectionCell.style.backgroundColor = '#00a65a'; // Dark Teal
        } else if (windDirection == "ENE") {
            windDirectionCell.style.backgroundColor = '#757575'; // Grey
        } else if (windDirection == "NNW") {
            windDirectionCell.style.backgroundColor = '#4285f6'; // Light Blue
        } else if (windDirection == "WNW") {
            windDirectionCell.style.backgroundColor = '#673ab7'; // Deep Purple
        } else if (windDirection == "SSE") {
            windDirectionCell.style.backgroundColor = '#d9534f'; // Dark Red
        } else if (windDirection == "ESE") {
            windDirectionCell.style.backgroundColor = '#20c997'; // Light Green
        } else if (windDirection == "SSW") {
            windDirectionCell.style.backgroundColor = '#ffb300'; // Amber
        } else if (windDirection == "WSW") {
            windDirectionCell.style.backgroundColor = '#00bcd4'; // Light Cyan
        } else {
            windDirectionCell.style.backgroundColor = '#ffffff'; // White
        }

        // Set color based on temperature value
        if (temp >= 45) {
        tempCell.style.backgroundColor = '#ff0000'; // Very hot (Red)
        } else if (temp == 44) {
        tempCell.style.backgroundColor = '#ff1a00'; 
        } else if (temp == 43) {
        tempCell.style.backgroundColor = '#ff3300'; 
        } else if (temp == 42) {
        tempCell.style.backgroundColor = '#ff4d00'; 
        } else if (temp == 41) {
        tempCell.style.backgroundColor = '#ff6600'; 
        } else if (temp == 40) {
        tempCell.style.backgroundColor = '#ff8000'; 
        } else if (temp == 39) {
        tempCell.style.backgroundColor = '#ff9900'; 
        } else if (temp == 38) {
        tempCell.style.backgroundColor = '#ffb300'; 
        } else if (temp == 37) {
        tempCell.style.backgroundColor = '#ffcc00'; 
        } else if (temp == 36) {
        tempCell.style.backgroundColor = '#ffe500'; 
        } else if (temp == 35) {
        tempCell.style.backgroundColor = '#ffff00'; 
        } else if (temp == 34) {
        tempCell.style.backgroundColor = '#e5ff00';
        } else if (temp == 33) {
        tempCell.style.backgroundColor = '#ccff00'; 
        } else if (temp == 32) {
        tempCell.style.backgroundColor = '#b3ff00';
        } else if (temp == 31) {
        tempCell.style.backgroundColor = '#99ff00';
        } else if (temp == 30) {
        tempCell.style.backgroundColor = '#80ff00'; 
        } else if (temp == 29) {
        tempCell.style.backgroundColor = '#66ff00'; 
        } else if (temp == 28) {
        tempCell.style.backgroundColor = '#4dff00'; 
        } else if (temp == 27) {
        tempCell.style.backgroundColor = '#33ff00'; 
        } else if (temp == 26) {
        tempCell.style.backgroundColor = '#1aff00'; 
        } else if (temp == 25) {
        tempCell.style.backgroundColor = '#00ff00'; 
        } else if (temp == 24) {
        tempCell.style.backgroundColor = '#00ff1a'; 
        } else if (temp == 23) {
        tempCell.style.backgroundColor = '#00ff33'; 
        } else if (temp == 22) {
        tempCell.style.backgroundColor = '#00ff4d';
        } else if (temp == 21) {
        tempCell.style.backgroundColor = '#00ff66'; 
        } else if (temp == 20) {
        tempCell.style.backgroundColor = '#00ff80'; 
        } else if (temp == 19) {
        tempCell.style.backgroundColor = '#00ff99';
        } else if (temp == 18) {
        tempCell.style.backgroundColor = '#00ffb3'; 
        } else if (temp == 17) {
        tempCell.style.backgroundColor = '#00ffcc';
        } else if (temp == 16) {
        tempCell.style.backgroundColor = '#00ffe5';
        } else if (temp == 15) {
        tempCell.style.backgroundColor = '#00ffff'; 
        } else if (temp == 14) {
        tempCell.style.backgroundColor = '#00e5ff'; 
        } else if (temp == 13) {
        tempCell.style.backgroundColor = '#00ccff';
        } else if (temp == 12) {
        tempCell.style.backgroundColor = '#00b3ff'; 
        } else if (temp == 11) {
        tempCell.style.backgroundColor = '#0099ff';
        } else if (temp == 10) {
        tempCell.style.backgroundColor = '#0080ff';
        } else if (temp == 9) {
        tempCell.style.backgroundColor = '#0066ff'; 
        } else if (temp == 8) {
        tempCell.style.backgroundColor = '#004dff';
        } else if (temp == 7) {
        tempCell.style.backgroundColor = '#0033ff'; 
        } else if (temp == 6) {
        tempCell.style.backgroundColor = '#001aff';
        } else {
        tempCell.style.backgroundColor = '#0000ff'; 
        }

        if (soilMoisture >= 100) {
        soilMoistureCell.style.backgroundColor = '#1B5E20'; // Dark green - High soil moisture
        } else if (soilMoisture >= 90) {
        soilMoistureCell.style.backgroundColor = '#2E7D32'; // Interpolate between high and moderate
        } else if (soilMoisture >= 80) {
        soilMoistureCell.style.backgroundColor = '#388E3C'; // Interpolate between high and moderate
        } else if (soilMoisture >= 70) {
        soilMoistureCell.style.backgroundColor = '#4CAF50'; // Interpolate between high and moderate
        } else if (soilMoisture >= 60) {
        soilMoistureCell.style.backgroundColor = '#66BB6A'; // Interpolate between high and moderate
        } else if (soilMoisture >= 50) {
        soilMoistureCell.style.backgroundColor = '#81C784'; // Moderate soil moisture - Light green
        } else if (soilMoisture >= 40) {
        soilMoistureCell.style.backgroundColor = '#9CCC65'; // Interpolate between moderate and low
        } else if (soilMoisture >= 30) {
        soilMoistureCell.style.backgroundColor = '#B2DFDB'; // Interpolate between moderate and low
        } else if (soilMoisture >= 20) {
        soilMoistureCell.style.backgroundColor = '#C8E6C9'; // Interpolate between moderate and low
        } else if (soilMoisture >= 10) {
        soilMoistureCell.style.backgroundColor = '#D8E6D5'; // Interpolate between moderate and low
        } else {
        soilMoistureCell.style.backgroundColor = '#E8F5E9'; // Lightest green - Low soil moisture
        }

        // Add additional coloring rules for other parameters as needed
    });
});

function generateLabels(station) {
    if (station === "NUTECH") {
        return TodayDataNUTECH.map(dataPoint => dataPoint.Time);
    } else {
        return TodayDataMARGALLA.map(dataPoint => dataPoint.Time);
    }
}
    
function generateLabelsNUTECH() {
    return TodayDataNUTECH.map(dataPoint => dataPoint.Time);
}
function getDataNUTECH(parameter) {
    return TodayDataNUTECH.map(dataPoint => parseFloat(dataPoint[parameter]));
}


// Function to generate random data for the graphs
function generateRandomData(min, max) {
    const data = [];
    for (let i = 0; i < 96; i++) { // 96 intervals for a full day (15 minutes each)
        data.push(Math.floor(Math.random() * (max - min + 1)) + min);
    }
    return data;
}


// Chart configuration with actual temperature data
const temperatureDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Temperature',
        data: getDataNUTECH("Temperature"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }]
};

const pressureDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Pressure',
        data: getDataNUTECH("Pressure"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }]
};

const windDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Wind Speed',
        data: getDataNUTECH("Wind_Speed"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const humidityDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Humidity',
        data: getDataNUTECH("Humidity"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }]
};

const rainDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Rain',
        data: getDataNUTECH("Rain"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }]
};

const solarradiationDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Solar Radiation',
        data: getDataNUTECH("Solar_Radiation"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const soilmoistureDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Soil Moisture',
        data: getDataNUTECH("Soil_Moisture"),
        borderColor: 'rgb(144, 238, 144)', // Light Green
        backgroundColor: 'rgba(144, 238, 144, 0.2)', // Light Green Shadow
        tension: 0.1,
        fill: true
    }]
};

const evapotranspirationDataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Evapotranspiration',
        data: getDataNUTECH("Evapotranspiration"),
        borderColor: 'rgb(0, 255, 255)', // Cyan
        backgroundColor: 'rgba(0, 255, 255, 0.2)', // Cyan Shadow
        tension: 0.1,
        fill: true
    }]
};

const co2DataNutech = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'CO2',
        data: getDataNUTECH("CO2_level"),
        borderColor: 'rgb(64, 224, 208)', // Turquoise
        backgroundColor: 'rgba(64, 224, 208, 0.2)', // Turquoise Shadow
        tension: 0.1,
        fill: true
    }]
};


// Create Chart configurations
const configTemplate = {
    type: 'line',
    options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 2, // Adjust the aspect ratio (default is 2, you can increase or decrease this value)
        scales: {
            y: {
                beginAtZero: false,
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)' // Lighter grid lines for better visibility
                },
                ticks: {
                    color: '#FFFFFF' // Make sure tick labels are visible
                }
            },
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)' // Same for x-axis grid lines
                },
                ticks: {
                    color: '#FFFFFF' // Make sure tick labels are visible
                }
            }
        },
        plugins: {
            legend: {
                display: false // Hide the legend
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.7)', // Darker tooltip background
                titleColor: '#FFFFFF',
                bodyColor: '#FFFFFF',
                borderColor: '#FFFFFF',
                borderWidth: 1
            },
            hover: {
                mode: 'nearest',
                intersect: true,
                animationDuration: 400 // Smooth hover animation
            }
        },
        layout: {
            padding: {
                left: 10,
                right: 10,
                top: 20,
                bottom: 5
            }
        }
    }
};

// Create Graphs
const temperatureChartNutech = new Chart(document.getElementById('temperatureGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: temperatureDataNutech
});
const pressureChartNutech = new Chart(document.getElementById('pressureGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: pressureDataNutech
});
const windSpeedChartNutech = new Chart(document.getElementById('windSpeedGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: windDataNutech
});
const humidityChartNutech = new Chart(document.getElementById('humidityGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: humidityDataNutech
});
const rainChartNutech = new Chart(document.getElementById('rainGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: rainDataNutech
});
const solarradiationChartNutech = new Chart(document.getElementById('solarradiationGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: solarradiationDataNutech
});
const soilmoistureChartNutech = new Chart(document.getElementById('soilmoistureGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: soilmoistureDataNutech
});
const evapotranspirationChartNutech = new Chart(document.getElementById('evapotranspirationGraphNutech').getContext('2d'), {
    ...configTemplate,
    data: evapotranspirationDataNutech
});
const co2ChartNutech = new Chart(document.getElementById('co2GraphNutech').getContext('2d'), {
    ...configTemplate,
    data: co2DataNutech
});

// Update graph data every 15 seconds
setInterval(() => {}, 15000);


function generateLabelsMARGALLA() {
    return TodayDataMARGALLA.map(dataPoint => dataPoint.Time);
}
function getDataMARGALLA(parameter) {
    return TodayDataMARGALLA.map(dataPoint => parseFloat(dataPoint[parameter]));
}

const temperatureDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        data: getDataMARGALLA("Temperature"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }]
};

const pressureDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        data: getDataMARGALLA("Pressure"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }]
};

const windDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        data: getDataMARGALLA("Wind_Speed"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const humidityDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        data: getDataMARGALLA("Humidity"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }]
};

const rainDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        data: getDataMARGALLA("Rain"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }]
};

const solarradiationDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        label: 'UV',
        data: getDataMARGALLA("Solar_Radiation"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const soilmoistureDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        label: 'Solar',
        data: getDataMARGALLA("Soil_Moisture"),
        borderColor: 'rgb(144, 238, 144)', // Light Green
        backgroundColor: 'rgba(144, 238, 144, 0.2)', // Light Green Shadow
        tension: 0.1,
        fill: true
    }]
};

const evapotranspirationDataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        label: 'Evapotranspiration',
        data: getDataMARGALLA("Evapotranspiration"),
        borderColor: 'rgb(0, 255, 255)', // Cyan
        backgroundColor: 'rgba(0, 255, 255, 0.2)', // Cyan Shadow
        tension: 0.1,
        fill: true
    }]
};

const co2DataMargalla = {
    labels: generateLabelsMARGALLA(),
    datasets: [{
        label: 'Optical Particles',
        data: getDataMARGALLA("CO2_level"),
        borderColor: 'rgb(64, 224, 208)', // Turquoise
        backgroundColor: 'rgba(64, 224, 208, 0.2)', // Turquoise Shadow
        tension: 0.1,
        fill: true
    }]
};  

const temperatureChartMargalla = new Chart(document.getElementById('temperatureGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: temperatureDataMargalla
});

const pressureChartMargalla = new Chart(document.getElementById('pressureGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: pressureDataMargalla
});

const windSpeedChartMargalla = new Chart(document.getElementById('windSpeedGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: windDataMargalla
});

const humidityChartMargalla = new Chart(document.getElementById('humidityGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: humidityDataMargalla
}); 

const rainChartMargalla = new Chart(document.getElementById('rainGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: rainDataMargalla
});

const solarradiationChartMargalla = new Chart(document.getElementById('solarradiationGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: solarradiationDataMargalla
});

const soilmoistureChartMargalla = new Chart(document.getElementById('soilmoistureGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: soilmoistureDataMargalla
});

const evapotranspirationChartMargalla = new Chart(document.getElementById('evapotranspirationGraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: evapotranspirationDataMargalla
});

const co2ChartMargalla = new Chart(document.getElementById('co2GraphMargalla').getContext('2d'), {
    ...configTemplate,
    data: co2DataMargalla
});

setInterval(() => {}, 15000);

const dualLineConfigTemplate = {
    type: 'line',
    options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 2, // Adjust the aspect ratio
        scales: {
            y: {
                beginAtZero: false,
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)' // Lighter grid lines for better visibility
                },
                ticks: {
                    color: '#FFFFFF' // Ensure tick labels are visible
                }
            },
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)' // Same for x-axis grid lines
                },
                ticks: {
                    color: '#FFFFFF' // Ensure tick labels are visible
                }
            }
        },
        plugins: {
            legend: {
                display: true, // Enable the legend
                labels: {
                    color: '#FFFFFF' // Legend label color
                },
                position: 'top' // Position the legend ('top', 'bottom', 'left', 'right')
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.7)', // Darker tooltip background
                titleColor: '#FFFFFF',
                bodyColor: '#FFFFFF',
                borderColor: '#FFFFFF',
                borderWidth: 1
            },
            hover: {
                mode: 'nearest',
                intersect: true,
                animationDuration: 400 // Smooth hover animation
            }
        },
        layout: {
            padding: {
                left: 10,
                right: 10,
                top: 10,
                bottom: 5
            }
        }
    }
};

const temperatureDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Temperature"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Temperature"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
}

const pressureDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Pressure"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Pressure"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
}

const windDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Wind_Speed"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Wind_Speed"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }]
}

const humidityDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Humidity"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Humidity"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }]
}

const rainDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Rain"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Rain"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
}

const solarradiationDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Solar_Radiation"),
        borderColor: 'rgb(0, 255, 255)', // Cyan
        backgroundColor: 'rgba(0, 255, 255, 0.2)', // Cyan Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Solar_Radiation"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
}

const soilmoistureDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Soil_Moisture"),
        borderColor: 'rgb(144, 238, 144)', // Light Green
        backgroundColor: 'rgba(144, 238, 144, 0.2)', // Light Green Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Soil_Moisture"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
}

const evapotranspirationDataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("Evapotranspiration"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("Evapotranspiration"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }]
}

const co2DataDaily = {
    labels: generateLabelsNUTECH(),
    datasets: [{
        label: 'Nutech',
        data: getDataNUTECH("CO2_level"),
        borderColor: 'rgb(64, 224, 208)', // Turquoise
        backgroundColor: 'rgba(64, 224, 208, 0.2)', // Turquoise Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getDataMARGALLA("CO2_level"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
}           

const temperatureChartDaily = new Chart(document.getElementById('temperatureGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: temperatureDataDaily
});

const pressureChartDaily = new Chart(document.getElementById('pressureGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: pressureDataDaily
});

const windSpeedChartDaily = new Chart(document.getElementById('windSpeedGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: windDataDaily
});

const humidityChartDaily = new Chart(document.getElementById('humidityGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: humidityDataDaily
});

const rainChartDaily = new Chart(document.getElementById('rainGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: rainDataDaily
});

const solarradiationChartDaily = new Chart(document.getElementById('solarradiationGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: solarradiationDataDaily
});

const soilmoistureChartDaily = new Chart(document.getElementById('soilmoistureGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: soilmoistureDataDaily
});

const evapotranspirationChartDaily = new Chart(document.getElementById('evapotranspirationGraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: evapotranspirationDataDaily
});

const co2ChartDaily = new Chart(document.getElementById('co2GraphDaily').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: co2DataDaily
});


function generateLabelsWeekly() {
    return WeeklyDataNUTECH.map(dataPoint => dataPoint.CollectionDate);
}
function getWeeklyDataNUTECH(parameter) {
    const x_data_week = generateLabelsWeekly();
    return x_data_week.map(date => {
        const value = AggregatedWeeklyDataNUTECH[`${date}_${parameter}`];
        return parseFloat(value);
    });

}
function getWeeklyDataMARGALLA(parameter) {
    const x_data_week = generateLabelsWeekly();
    return x_data_week.map(date => {
        const value = AggregatedWeeklyDataMargalla[`${date}_${parameter}`];
        return parseFloat(value);
    });

}

const temperatureDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Temperature"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Temperature"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const pressureDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Pressure"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Pressure"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const windDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Wind_Speed"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Wind_Speed"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }]
};

const humidityDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Humidity"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Humidity"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }]
};

const rainDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Rain"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Rain"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const solarradiationDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Solar_Radiation"),
        borderColor: 'rgb(0, 255, 255)', // Cyan
        backgroundColor: 'rgba(0, 255, 255, 0.2)', // Cyan Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Solar_Radiation"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const soilmoistureDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Soil_Moisture"),
        borderColor: 'rgb(144, 238, 144)', // Light Green
        backgroundColor: 'rgba(144, 238, 144, 0.2)', // Light Green Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Soil_Moisture"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const evapotranspirationDataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("Evapotranspiration"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("Evapotranspiration"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }]
};

const co2DataWeekly = {
    labels: generateLabelsWeekly(),
    datasets: [{
        label: 'Nutech',
        data: getWeeklyDataNUTECH("CO2_level"),
        borderColor: 'rgb(64, 224, 208)', // Turquoise
        backgroundColor: 'rgba(64, 224, 208, 0.2)', // Turquoise Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getWeeklyDataMARGALLA("CO2_level"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const temperatureChartWeekly = new Chart(document.getElementById('temperatureGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: temperatureDataWeekly
});

const pressureChartWeekly = new Chart(document.getElementById('pressureGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: pressureDataWeekly
});

const windSpeedChartWeekly = new Chart(document.getElementById('windSpeedGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: windDataWeekly
});

const humidityChartWeekly = new Chart(document.getElementById('humidityGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: humidityDataWeekly
});

const rainChartWeekly = new Chart(document.getElementById('rainGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: rainDataWeekly
});

const solarradiationChartWeekly = new Chart(document.getElementById('solarradiationGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: solarradiationDataWeekly
});

const soilmoistureChartWeekly = new Chart(document.getElementById('soilmoistureGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: soilmoistureDataWeekly
});

const evapotranspirationChartWeekly = new Chart(document.getElementById('evapotranspirationGraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: evapotranspirationDataWeekly
});

const co2ChartWeekly = new Chart(document.getElementById('co2GraphWeekly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: co2DataWeekly
});
function generateLabelsMonthly(){
    return Monthly_Graphs_Labels.map(dataPoint => dataPoint.CollectionDate);
}

function getMonthlyDataNUTECH(parameter) {
    const x_data_month = generateLabelsMonthly();
    return x_data_month.map(date => {
        const value = Monthly_Graphs_Data_NUTECH[`${date}_${parameter}`];
        return parseFloat(value);
    });
}

function getMonthlyDataMARGALLA(parameter) {
    const x_data_month = generateLabelsMonthly();
    return x_data_month.map(date => {
        const value = Monthly_Graphs_Data_MARGALLA[`${date}_${parameter}`];
        return parseFloat(value);
    });
}

const temperatureDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Temperature"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Temperature"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const pressureDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Pressure"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Pressure"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const windDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Wind_Speed"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Wind_Speed"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }]
};

const humidityDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Humidity"),
        borderColor: 'rgb(75, 192, 192)', // Light Blue
        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light Blue Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Humidity"),
        borderColor: 'rgb(153, 102, 255)', // Purple
        backgroundColor: 'rgba(153, 102, 255, 0.2)', // Purple Shadow
        tension: 0.1,
        fill: true
    }]
};

const rainDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Rain"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Rain"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const solarradiationDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Solar_Radiation"),
        borderColor: 'rgb(0, 255, 255)', // Cyan
        backgroundColor: 'rgba(0, 255, 255, 0.2)', // Cyan Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Solar_Radiation"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const soilmoistureDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Soil_Moisture"),
        borderColor: 'rgb(144, 238, 144)', // Light Green
        backgroundColor: 'rgba(144, 238, 144, 0.2)', // Light Green Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Soil_Moisture"),
        borderColor: 'rgb(255, 206, 86)', // Yellow
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Yellow Shadow
        tension: 0.1,
        fill: true
    }]
};

const evapotranspirationDataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("Evapotranspiration"),
        borderColor: 'rgb(255, 159, 64)', // Orange
        backgroundColor: 'rgba(255, 159, 64, 0.2)', // Orange Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("Evapotranspiration"),
        borderColor: 'rgb(54, 162, 235)', // Blue
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Blue Shadow
        tension: 0.1,
        fill: true
    }]
};

const co2DataMonthly = {
    labels: generateLabelsMonthly(),
    datasets: [{
        label: 'Nutech',
        data: getMonthlyDataNUTECH("CO2_level"),
        borderColor: 'rgb(64, 224, 208)', // Turquoise
        backgroundColor: 'rgba(64, 224, 208, 0.2)', // Turquoise Shadow
        tension: 0.1,
        fill: true
    }, {
        label: 'Margalla',
        data: getMonthlyDataMARGALLA("CO2_level"),
        borderColor: 'rgb(255, 99, 132)', // Red
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Red Shadow
        tension: 0.1,
        fill: true
    }]
};

const temperatureChartMonthly = new Chart(document.getElementById('temperatureGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: temperatureDataMonthly
});

const pressureChartMonthly = new Chart(document.getElementById('pressureGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: pressureDataMonthly
});

const windSpeedChartMonthly = new Chart(document.getElementById('windSpeedGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: windDataMonthly
});

const humidityChartMonthly = new Chart(document.getElementById('humidityGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: humidityDataMonthly
});

const rainChartMonthly = new Chart(document.getElementById('rainGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: rainDataMonthly
});

const solarradiationChartMonthly = new Chart(document.getElementById('solarradiationGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: solarradiationDataMonthly
});

const soilmoistureChartMonthly = new Chart(document.getElementById('soilmoistureGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: soilmoistureDataMonthly
});

const evapotranspirationChartMonthly = new Chart(document.getElementById('evapotranspirationGraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: evapotranspirationDataMonthly
});

const co2ChartMonthly = new Chart(document.getElementById('co2GraphMonthly').getContext('2d'), {
    ...dualLineConfigTemplate,
    data: co2DataMonthly
<<<<<<< HEAD
});
=======
});

console.log(TodayData);
>>>>>>> d6eb8847b9f0289418c744ba86fad811561abc03
