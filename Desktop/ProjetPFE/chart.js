document.addEventListener('DOMContentLoaded', function() {
    // Exemple de données pour le graphique de tendance des niveaux
    var waterLevelCtx = document.getElementById('waterLevelChart').getContext('2d');
    var waterLevelChart = new Chart(waterLevelCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
            datasets: [{
                label: 'Niveau moyen (%)',
                data: [65, 63, 66, 62, 68, 67],
                borderColor: '#007bff',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Exemple de données pour le graphique de prédictions
    var predictionCtx = document.getElementById('predictionChart').getContext('2d');
    var predictionChart = new Chart(predictionCtx, {
        type: 'bar',
        data: {
            labels: ['Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
            datasets: [{
                label: 'Prévision du niveau (%)',
                data: [66, 64, 60, 58, 62, 65],
                backgroundColor: '#28a745'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Exemple de données pour le graphique des facteurs de risque
    var riskFactorsCtx = document.getElementById('riskFactorsChart').getContext('2d');
    var riskFactorsChart = new Chart(riskFactorsCtx, {
        type: 'pie',
        data: {
            labels: ['Faible pluie', 'Surpompage', 'Pollution'],
            datasets: [{
                data: [40, 30, 30],
                backgroundColor: ['#ffc107', '#dc3545', '#007bff']
            }]
        }
    });
});