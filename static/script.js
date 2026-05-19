document.addEventListener('DOMContentLoaded', () => {

    // --- File Upload UI Logic ---
    document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
        const dropZoneElement = inputElement.closest(".drop-zone");

        dropZoneElement.addEventListener("click", (e) => {
            inputElement.click();
        });

        inputElement.addEventListener("change", (e) => {
            if (inputElement.files.length) {
                updateThumbnail(dropZoneElement, inputElement.files[0]);
            }
        });

        dropZoneElement.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZoneElement.classList.add("drop-zone--over");
        });

        ["dragleave", "dragend"].forEach((type) => {
            dropZoneElement.addEventListener(type, (e) => {
                dropZoneElement.classList.remove("drop-zone--over");
            });
        });

        dropZoneElement.addEventListener("drop", (e) => {
            e.preventDefault();

            if (e.dataTransfer.files.length) {
                inputElement.files = e.dataTransfer.files;
                updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
            }

            dropZoneElement.classList.remove("drop-zone--over");
        });
    });

    function updateThumbnail(dropZoneElement, file) {
        let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

        // First time - remove the prompt
        if (dropZoneElement.querySelector(".drop-zone__prompt")) {
            dropZoneElement.querySelector(".drop-zone__prompt").remove();
        }

        // First time - there is no thumbnail element, so lets create it
        if (!thumbnailElement) {
            thumbnailElement = document.createElement("div");
            thumbnailElement.classList.add("drop-zone__thumb");
            dropZoneElement.appendChild(thumbnailElement);
        }

        thumbnailElement.dataset.label = file.name;

        // Show thumbnail for image files
        if (file.type.startsWith("image/")) {
            const reader = new FileReader();

            reader.readAsDataURL(file);
            reader.onload = () => {
                thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
            };
        } else if (file.type === "application/pdf") {
            thumbnailElement.style.backgroundImage = null;
            thumbnailElement.innerHTML = '<i class="fa-solid fa-file-pdf" style="font-size: 3rem; color: #ef4444; margin-top: 20px;"></i>';
        } else {
            thumbnailElement.style.backgroundImage = null;
            thumbnailElement.innerHTML = '<i class="fa-solid fa-file" style="font-size: 3rem; color: #6366f1; margin-top: 20px;"></i>';
        }
    }

    // --- Toggle Logic ---
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            toggleBtns.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.key-input-mode').forEach(el => el.classList.remove('active'));

            // Add active to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // --- Form Submission Logic ---
    const form = document.getElementById('evaluationForm');
    const loadingState = document.getElementById('loadingState');
    const resultState = document.getElementById('resultState');
    const errorState = document.getElementById('errorState');
    const formContainer = document.querySelector('.form-container');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Basic validation
        const hasText = document.getElementById('answer_key_text').value.trim() !== '';
        const hasFile = document.getElementById('answer_key_file').files.length > 0;

        if (!hasText && !hasFile) {
            alert("Please provide the Answer Key (either text or upload a file).");
            return;
        }

        const formData = new FormData(form);

        // UI transitions
        formContainer.classList.add('hidden');
        loadingState.classList.remove('hidden');

        // Faking step progression for UX (since API is monolithic)
        animateSteps();

        try {
            const response = await fetch('/evaluate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Evaluation failed on the server.");
            }

            // Populate Results
            document.getElementById('finalScore').innerText = data.final_score;
            document.getElementById('maxScore').innerText = data.max_marks;
            document.getElementById('resRollNumber').innerText = data.roll_number;

            const confidenceSpan = document.getElementById('resConfidence');
            confidenceSpan.innerText = data.confidence;
            confidenceSpan.className = `badge ${data.confidence}`;

            document.getElementById('resRawMarks').innerText = `${data.details.obtained_raw} / ${data.details.possible_raw}`;

            // Show Results
            loadingState.classList.add('hidden');
            resultState.classList.remove('hidden');

        } catch (error) {
            console.error(error);
            document.getElementById('errorMessage').innerText = error.message;
            loadingState.classList.add('hidden');
            errorState.classList.remove('hidden');
        }
    });

    function animateSteps() {
        const steps = document.querySelectorAll('.step');
        let current = 0;

        // Just a simple visual fake for the monolithic call
        const interval = setInterval(() => {
            if (current < steps.length - 1) {
                steps[current].classList.remove('active');
                current++;
                steps[current].classList.add('active');
            } else {
                clearInterval(interval);
            }
        }, 5000); // Change step every 5 seconds roughly
    }

    // --- Reset Logic ---
    document.getElementById('resetBtn').addEventListener('click', resetForm);
    document.getElementById('errorResetBtn').addEventListener('click', resetForm);

    function resetForm() {
        form.reset();

        // Reset Dropzones
        document.querySelectorAll('.drop-zone__thumb').forEach(thumb => thumb.remove());
        document.querySelectorAll('.drop-zone').forEach(zone => {
            if (!zone.querySelector('.drop-zone__prompt')) {
                const prompt = document.createElement('span');
                prompt.className = 'drop-zone__prompt';
                prompt.innerText = 'Drop file here or click to upload';
                zone.prepend(prompt);
            }
        });

        // Toggle visibility
        resultState.classList.add('hidden');
        errorState.classList.add('hidden');
        formContainer.classList.remove('hidden');

        // Reset steps
        const steps = document.querySelectorAll('.step');
        steps.forEach(s => s.classList.remove('active'));
        steps[0].classList.add('active');
    }
});
