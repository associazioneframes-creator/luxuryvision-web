<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>LuxuryVision | Pro Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0a0a0a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.03); border: 1px solid #333; backdrop-filter: blur(10px); }
        .gold-accent { border-color: #d4af37; }
        .text-gold { color: #d4af37; }
    </style>
</head>
<body class="p-8">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-light tracking-widest text-gold mb-8">LUXURYVISION</h1>
        
        <div class="grid grid-cols-3 gap-6">
            <!-- Colonna Sinistra -->
            <div class="col-span-2 space-y-6">
                <!-- Area Drop/Paste -->
                <div id="dropZone" class="glass h-64 flex flex-col items-center justify-center border-2 border-dashed border-gray-700 hover:border-gold-accent transition cursor-pointer rounded-xl">
                    <img id="preview" class="max-h-52 hidden rounded" alt="Preview">
                    <div id="placeholder" class="text-center">
                        <p class="text-gray-400">Trascina un file o <b>CTRL+V</b> per incollare</p>
                    </div>
                </div>

                <textarea id="notes" class="w-full bg-black border border-gray-700 p-4 rounded-xl focus:border-gold-accent outline-none" placeholder="Note per l'AI..."></textarea>
                <button onclick="analyze()" class="w-full py-4 bg-gold-accent text-black font-bold rounded-xl hover:bg-yellow-600 transition">ANALIZZA PROMPT</button>
            </div>

            <!-- Colonna Destra (Anteprime e Risultati) -->
            <div class="glass p-6 rounded-xl">
                <h2 class="text-gold font-bold mb-4">OUTPUT</h2>
                <div id="output" class="text-sm italic text-gray-400">In attesa...</div>
            </div>
        </div>
    </div>

    <script>
        let uploadedFile = null;

        // Gestione Incolla (CTRL+V)
        window.addEventListener('paste', e => {
            const item = e.clipboardData.items[0];
            if (item.type.startsWith('image')) {
                const file = item.getAsFile();
                processImage(file);
            }
        });

        function processImage(file) {
            uploadedFile = file;
            const reader = new FileReader();
            reader.onload = e => {
                document.getElementById('preview').src = e.target.result;
                document.getElementById('preview').classList.remove('hidden');
                document.getElementById('placeholder').classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }

        async function analyze() {
            if (!uploadedFile) { alert("Carica un'immagine prima!"); return; }
            const formData = new FormData();
            formData.append('image', uploadedFile);
            formData.append('notes', document.getElementById('notes').value);
            
            document.getElementById('output').innerText = "Elaborazione in corso...";
            const res = await fetch('/api/analyze', { method: 'POST', body: formData });
            const data = await res.json();
            document.getElementById('output').innerText = data.prompt || data.error;
        }
    </script>
</body>
</html>
