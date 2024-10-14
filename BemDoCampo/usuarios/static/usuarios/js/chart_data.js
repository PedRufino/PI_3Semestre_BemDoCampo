var ctx2 = document.getElementById("chart-line").getContext("2d");

var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);
var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

new Chart(ctx2, {
type: "line",
data: {
    labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [{
        label: "Mobile apps",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        borderColor: "#109c00",
        borderWidth: 3,
        backgroundColor: gradientStroke1,
        fill: true,
        data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
        maxBarThickness: 6
    },
    {
        label: "Cu1",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        borderColor: "#fd9800",
        borderWidth: 3,
        backgroundColor: gradientStroke2,
        fill: true,
        data: [499, 262, 181, 23, 149, 327, 141, 131, 361, 428],
        maxBarThickness: 6
    },
    {
        label: "Websites",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        borderColor: "#4d9b00",
        borderWidth: 3,
        backgroundColor: gradientStroke2,
        fill: true,
        data: [30, 90, 40, 140, 290, 290, 340, 230, 400],
        maxBarThickness: 6
    },
    {
        label: "C2",
        tension: 0.4,
        borderWidth: 0,
        pointRadius: 0,
        borderColor: "#d78f00",
        borderWidth: 3,
        backgroundColor: gradientStroke2,
        fill: true,
        data: [286, 172, 157, 82, 259, 16, 164, 290, 308],
        maxBarThickness: 6
    },
    ],
},
options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
    legend: {
        display: false,
    }
    },
    interaction: {
    intersect: false,
    mode: 'index',
    },
    scales: {
    y: {
        grid: {
        drawBorder: false,
        display: true,
        drawOnChartArea: true,
        drawTicks: false,
        borderDash: [5, 5]
        },
        ticks: {
        display: true,
        padding: 10,
        color: '#b2b9bf',
        font: {
            size: 11,
            family: "Open Sans",
            style: 'normal',
            lineHeight: 2
        },
        }
    },
    x: {
        grid: {
        drawBorder: false,
        display: false,
        drawOnChartArea: false,
        drawTicks: false,
        borderDash: [5, 5]
        },
        ticks: {
        display: true,
        color: '#b2b9bf',
        padding: 20,
        font: {
            size: 11,
            family: "Open Sans",
            style: 'normal',
            lineHeight: 2
        },
        }
    },
    },
},
});