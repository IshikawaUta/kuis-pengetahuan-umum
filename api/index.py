from flask import Flask, render_template, request, redirect, url_for, session
import random
import os # Import modul os untuk mengakses environment variables

# Buat instance Flask
app = Flask(__name__, template_folder='../templates', static_folder='../static') # Tentukan lokasi templates dan static

# Set secret key dari Environment Variable Vercel
# Pastikan Anda mengatur SECRET_KEY di pengaturan Vercel
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key_jika_tidak_ada') # Gunakan fallback hanya untuk development lokal jika perlu

# Data Kuis (Kumpulan Pertanyaan Lebih Banyak)
quiz_data_pool = [
    {"question": "Apa ibu kota Indonesia?", "options": ["Surabaya", "Bandung", "Jakarta", "Yogyakarta"], "answer": "Jakarta"},
    {"question": "Planet terdekat dengan Matahari adalah?", "options": ["Mars", "Venus", "Bumi", "Merkurius"], "answer": "Merkurius"},
    {"question": "Siapa penemu lampu pijar?", "options": ["Nikola Tesla", "Isaac Newton", "Thomas Edison", "Galileo Galilei"], "answer": "Thomas Edison"},
    {"question": "Berapa jumlah benua di dunia?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "Apa warna bendera nasional Jepang?", "options": ["Merah dan Putih", "Hitam dan Kuning", "Biru dan Putih", "Hijau dan Merah"], "answer": "Merah dan Putih"},
    {"question": "Sungai terpanjang di dunia adalah?", "options": ["Sungai Amazon", "Sungai Nil", "Sungai Yangtze", "Sungai Mississippi"], "answer": "Sungai Nil"},
    {"question": "Hewan darat tercepat di dunia adalah?", "options": ["Singa", "Harimau", "Cheetah", "Leopard"], "answer": "Cheetah"},
    {"question": "Negara terbesar di dunia berdasarkan luas wilayah adalah?", "options": ["Kanada", "Tiongkok", "Amerika Serikat", "Rusia"], "answer": "Rusia"},
    {"question": "Berapa sisi yang dimiliki sebuah heptagon?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "Nama unsur kimia dengan simbol O adalah?", "options": ["Emas", "Oksigen", "Osmium", "Perak"], "answer": "Oksigen"},
    {"question": "Tahun berapa manusia pertama kali mendarat di Bulan?", "options": ["1965", "1969", "1971", "1975"], "answer": "1969"},
    {"question": "Nama samaran superhero Batman adalah?", "options": ["Clark Kent", "Peter Parker", "Bruce Wayne", "Tony Stark"], "answer": "Bruce Wayne"},
    {"question": "Instrumen musik dengan senar dan dimainkan dengan gesekan busur adalah?", "options": ["Gitar", "Biola", "Piano", "Drum"], "answer": "Biola"},
    {"question": "Berapa suhu air mendidih pada permukaan laut dalam Celcius?", "options": ["0", "50", "100", "200"], "answer": "100"},
    {"question": "Siapa penulis novel 'Romeo and Juliet'?", "options": ["Charles Dickens", "Jane Austen", "William Shakespeare", "Leo Tolstoy"], "answer": "William Shakespeare"}
    # Tambahkan lebih banyak pertanyaan di sini jika diinginkan
]

# Jumlah pertanyaan yang akan ditampilkan per kuis
NUM_QUESTIONS_PER_QUIZ = 5

@app.route('/')
def index():
    """Menampilkan halaman beranda."""
    # Melewatkan jumlah total pertanyaan di kolam ke template home
    return render_template('home.html', total_questions_pool=len(quiz_data_pool), num_questions_per_quiz=NUM_QUESTIONS_PER_QUIZ)

@app.route('/quiz')
def quiz_page():
    """Memilih 5 pertanyaan acak dan menampilkannya."""
    if len(quiz_data_pool) < NUM_QUESTIONS_PER_QUIZ:
        # Handle kasus jika jumlah pertanyaan di pool kurang dari yang diminta
        # Anda bisa menampilkan pesan error atau menggunakan semua pertanyaan yang ada
        questions_for_this_quiz = list(quiz_data_pool) # Menggunakan semua yang ada jika kurang dari 5
    else:
        # Pilih NUM_QUESTIONS_PER_QUIZ pertanyaan acak dari pool
        questions_for_this_quiz = random.sample(quiz_data_pool, NUM_QUESTIONS_PER_QUIZ)

    # Simpan urutan pertanyaan yang dipilih di session
    session['current_quiz_questions'] = questions_for_this_quiz

    # Tampilkan template kuis dengan 5 pertanyaan yang sudah dipilih
    return render_template('quiz.html', questions=questions_for_this_quiz)

@app.route('/submit', methods=['POST'])
def submit():
    """Memproses jawaban kuis dari 5 pertanyaan yang dipilih dan menampilkan hasil."""
    # Ambil urutan 5 pertanyaan yang dipilih dari session
    questions_for_this_quiz = session.get('current_quiz_questions')

    # Jika data session tidak ada (misal: user langsung ke /submit atau session expire)
    if not questions_for_this_quiz:
        # Redirect kembali ke halaman kuis untuk memulai ulang
        return redirect(url_for('quiz_page'))

    score = 0
    results = [] # Untuk menyimpan detail hasil setiap pertanyaan

    # Iterasi melalui 5 pertanyaan yang dipilih (dari session)
    for i, question_item in enumerate(questions_for_this_quiz):
        # Nama input radio di form adalah 'question_0', 'question_1', dst.,
        # sesuai dengan loop.index0 pada template quiz.html yang menggunakan data 5 pertanyaan ini.
        user_answer = request.form.get(f'question_{i}')
        correct_answer = question_item['answer']
        question_text = question_item['question']

        is_correct = (user_answer == correct_answer)

        results.append({
            "question": question_text,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })
        # Hitung skor setelah hasil ditambahkan
        if is_correct:
            score += 1


    # Hapus data kuis dari session setelah selesai
    session.pop('current_quiz_questions', None)

    # Render halaman hasil dengan skor dan detail hasil.
    # Total adalah jumlah pertanyaan di kuis ini (yaitu 5 atau len(questions_for_this_quiz))
    return render_template('result.html', score=score, total=len(questions_for_this_quiz), results=results)

# --- Bagian ini tidak diperlukan saat di-deploy ke Vercel ---
# if __name__ == '__main__':
#     app.run(debug=True)
# ----------------------------------------------------------