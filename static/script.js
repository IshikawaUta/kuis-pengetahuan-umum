// Anda bisa menambahkan kode JavaScript di sini nanti
// Contoh: Kode untuk memvalidasi form sebelum dikirim (pastikan semua pertanyaan dijawab)
// const form = document.getElementById('quizForm');
// form.addEventListener('submit', function(event) {
//     const requiredInputs = form.querySelectorAll('input[type="radio"][required]');
//     let allAnswered = true;
//     const questionNames = new Set();

//     requiredInputs.forEach(input => {
//         questionNames.add(input.name);
//     });

//     questionNames.forEach(name => {
//         const answered = form.querySelector(`input[name="${name}"]:checked`);
//         if (!answered) {
//             allAnswered = false;
//         }
//     });

//     if (!allAnswered) {
//         alert('Harap jawab semua pertanyaan sebelum mengirim.');
//         event.preventDefault(); // Mencegah form dikirim
//     }
// });
