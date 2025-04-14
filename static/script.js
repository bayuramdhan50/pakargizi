document.getElementById('nutritionForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const umur = document.getElementById('umur').value;
    const gender = document.getElementById('gender').value;

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ umur, gender })
        });

        const data = await response.json();

        if (data.status === 'success') {
            const outputDiv = document.getElementById('output');
            const kebutuhan = data.kebutuhan;
            const rekomendasi = data.rekomendasi;

            outputDiv.innerHTML = `
                <h3>Kebutuhan Gizi Harian</h3>
                <ul>
                    <li><strong>Kalori:</strong> ${kebutuhan.kalori} kkal</li>
                    <li><strong>Protein:</strong> ${kebutuhan.protein} gram</li>
                    <li><strong>Lemak:</strong> ${kebutuhan.lemak} gram</li>
                    <li><strong>Karbohidrat:</strong> ${kebutuhan.karbohidrat} gram</li>
                </ul>
                <h3>Rekomendasi Makanan</h3>
                <ul>
                    ${rekomendasi.map(m => {
                        const kandungan = Object.entries(m).filter(([k]) => k !== 'nama').map(([k, v]) => `${k}: ${v}g`).join(', ');
                        return `<li><strong>${m.nama}</strong> (${kandungan})</li>`;
                    }).join('')}
                </ul>
            `;

            document.getElementById('result').classList.remove('hidden');
        } else {
            alert("Terjadi kesalahan: " + data.message);
        }
    } catch (err) {
        alert("Gagal menghubungi server.");
        console.error(err);
    }
});
