function fetchLive() {

    fetch("/api/latest-data")
        .then(res => res.json())
        .then(data => {

            if (!data) return;

            const bpm = parseInt(data.bpm);
            const ecg = parseInt(data.ecg);

            if (!isNaN(bpm)) {
                updateUI(bpm);
            }

            if (!isNaN(ecg)) {
                window.addRealECG(ecg);
            }
        })
        .catch(err => console.log("API Error:", err));
}

setInterval(fetchLive, 2000);
fetchLive();