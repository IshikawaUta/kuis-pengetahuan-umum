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
  {
    "question": "Apakah ibu kota Prancis?",
    "options": ["Berlin", "Madrid", "Paris", "Roma"],
    "answer": "Paris"
  },
  {
    "question": "Siapakah presiden pertama Indonesia?",
    "options": ["Mohammad Hatta", "Sutan Sjahrir", "Soepomo", "Soekarno"],
    "answer": "Soekarno"
  },
  {
    "question": "Planet manakah yang paling dekat dengan Matahari?",
    "options": ["Venus", "Merkurius", "Bumi", "Mars"],
    "answer": "Merkurius"
  },
  {
    "question": "Apakah simbol kimia untuk air?",
    "options": ["H2O2", "CO2", "O2", "H2O"],
    "answer": "H2O"
  },
  {
    "question": "Siapakah yang menulis drama \"Romeo and Juliet\"?",
    "options": ["Charles Dickens", "Jane Austen", "Mark Twain", "William Shakespeare"],
    "answer": "William Shakespeare"
  },
  {
    "question": "Benua manakah yang terbesar di dunia?",
    "options": ["Afrika", "Asia", "Eropa", "Amerika Utara"],
    "answer": "Asia"
  },
  {
    "question": "Organ tubuh manakah yang memompa darah ke seluruh tubuh?",
    "options": ["Otak", "Paru-paru", "Ginjal", "Jantung"],
    "answer": "Jantung"
  },
  {
    "question": "Warna primer apa saja yang tidak dapat dibuat dengan mencampur warna lain?",
    "options": ["Hijau, Oranye, Ungu", "Merah, Biru, Kuning", "Putih, Hitam, Abu-abu", "Merah, Hijau, Biru"],
    "answer": "Merah, Biru, Kuning"
  },
  {
    "question": "Hewan manakah yang terkenal karena memiliki kantung (marsupial)?",
    "options": ["Harimau", "Gajah", "Kanguru", "Beruang"],
    "answer": "Kanguru"
  },
  {
    "question": "Bahasa apakah yang paling banyak digunakan di dunia (berdasarkan jumlah penutur asli)?",
    "options": ["Inggris", "Spanyol", "Hindi", "Mandarin"],
    "answer": "Mandarin"
  },
  {
    "question": "Pada tahun berapakah proklamasi kemerdekaan Indonesia dibacakan?",
    "options": ["1942", "1943", "1944", "1945"],
    "answer": "1945"
  },
  {
    "question": "Samudra manakah yang terbesar di dunia?",
    "options": ["Atlantik", "Hindia", "Arktik", "Pasifik"],
    "answer": "Pasifik"
  },
  {
    "question": "Berapakah jumlah benua di Bumi?",
    "options": ["5", "6", "7", "8"],
    "answer": "7"
  },
  {
    "question": "Siapakah penemu lampu pijar?",
    "options": ["Isaac Newton", "Thomas Edison", "Alexander Graham Bell", "Albert Einstein"],
    "answer": "Thomas Edison"
  },
  {
    "question": "Makanan pokok sebagian besar penduduk Indonesia adalah?",
    "options": ["Jagung", "Gandum", "Sagu", "Nasi"],
    "answer": "Nasi"
  },
  {
    "question": "Gunung tertinggi di dunia adalah?",
    "options": ["K2", "Kangchenjunga", "Lhotse", "Gunung Everest"],
    "answer": "Gunung Everest"
  },
  {
    "question": "Apakah satuan dasar pengukuran panjang dalam sistem metrik?",
    "options": ["Inch", "Kaki", "Yard", "Meter"],
    "answer": "Meter"
  },
  {
    "question": "Siapakah pelukis \"Mona Lisa\"?",
    "options": ["Vincent van Gogh", "Pablo Picasso", "Michelangelo", "Leonardo da Vinci"],
    "answer": "Leonardo da Vinci"
  },
  {
    "question": "Dalam olahraga sepak bola, berapa jumlah pemain dalam satu tim di lapangan?",
    "options": ["9", "10", "11", "12"],
    "answer": "11"
  },
  {
    "question": "Gas apakah yang paling melimpah di atmosfer Bumi?",
    "options": ["Oksigen", "Karbon Dioksida", "Argon", "Nitrogen"],
    "answer": "Nitrogen"
  },
  {
    "question": "Sungai terpanjang di dunia adalah?",
    "options": ["Sungai Amazon", "Sungai Nil", "Sungai Yangtze", "Sungai Mississippi"],
    "answer": "Sungai Nil"
  },
  {
    "question": "Berapakah hasil dari 7 x 9?",
    "options": ["56", "60", "63", "72"],
    "answer": "63"
  },
  {
    "question": "Lambang negara Indonesia adalah?",
    "options": ["Bendera Merah Putih", "Garuda Pancasila", "Pohon Beringin", "Padi dan Kapas"],
    "answer": "Garuda Pancasila"
  },
  {
    "question": "Alat musik tradisional dari Jawa Barat yang terbuat dari bambu adalah?",
    "options": ["Gamelan", "Angklung", "Kolintang", "Angklung"],
    "answer": "Angklung"
  },
  {
    "question": "Pada tanggal berapakah Hari Kemerdekaan Indonesia dirayakan setiap tahun?",
    "options": ["17 Agustus", "28 Oktober", "1 Mei", "10 November"],
    "answer": "17 Agustus"
  },
  {
    "question": "Hewan manakah yang dikenal sebagai \"raja hutan\"?",
    "options": ["Harimau", "Gajah", "Singa", "Beruang"],
    "answer": "Singa"
  },
  {
    "question": "Planet manakah yang terkenal dengan cincinnya?",
    "options": ["Mars", "Jupiter", "Saturnus", "Uranus"],
    "answer": "Saturnus"
  },
  {
    "question": "Apakah mata uang negara Jepang?",
    "options": ["Won", "Yuan", "Baht", "Yen"],
    "answer": "Yen"
  },
  {
    "question": "Teori relativitas dikembangkan oleh siapa?",
    "options": ["Isaac Newton", "Stephen Hawking", "Albert Einstein", "Galileo Galilei"],
    "answer": "Albert Einstein"
  },
  {
    "question": "Cabang olahraga bela diri yang berasal dari Indonesia adalah?",
    "options": ["Karate", "Taekwondo", "Kung Fu", "Pencak Silat"],
    "answer": "Pencak Silat"
  },
  {
    "question": "Berapakah jumlah sisi pada segitiga?",
    "options": ["2", "3", "4", "5"],
    "answer": "3"
  },
  {
    "question": "Film animasi pertama yang sepenuhnya dibuat dengan grafik komputer adalah?",
    "options": ["Snow White and the Seven Dwarfs", "Toy Story", "The Lion King", "Tom & jerry"],
    "answer": "Toy Story"
  },
  {
    "question": "Siapakah penemu telepon?",
    "options": ["Guglielmo Marconi", "Alexander Graham Bell", "Nikola Tesla", "Thomas Edison"],
    "answer": "Alexander Graham Bell"
  },
  {
    "question": "Apa nama ibu kota Australia?",
    "options": ["Sydney", "Melbourne", "Brisbane", "Canberra"],
    "answer": "Canberra"
  },
  {
    "question": "Apa nama benda langit yang mengelilingi Matahari?",
    "options": ["Bintang", "Bulan", "Komet", "Planet"],
    "answer": "Planet"
  },
  {
    "question": "Tarian tradisional dari Bali yang menggambarkan pertempuran antara kebaikan (Barong) dan kejahatan (Rangda) adalah?",
    "options": ["Tari Saman", "Tari Piring", "Tari Kecak", "Tari Barong"],
    "answer": "Tari Barong"
  },
  {
    "question": "Berapakah titik beku air dalam skala Celsius?",
    "options": ["100°C", "-10°C", "0°C", "10°C"],
    "answer": "0°C"
  },
  {
    "question": "Lautan apakah yang memisahkan Eropa dan Afrika dari Amerika?",
    "options": ["Pasifik", "Atlantik", "Hindia", "Arktik"],
    "answer": "Atlantik"
  },
  {
    "question": "Siapakah penulis novel \"Harry Potter\"?",
    "options": ["Stephen King", "George R.R. Martin", "J.K. Rowling", "Suzanne Collins"],
    "answer": "J.K. Rowling"
  },
  {
    "question": "Olahraga apakah yang menggunakan bola dan dimainkan di atas es dengan menggunakan tongkat?",
    "options": ["Basket", "Voli", "Hoki Es", "Polo Air"],
    "answer": "Hoki Es"
  },
  {
    "question": "Berapakah jumlah warna pada pelangi?",
    "options": ["5", "6", "7", "8"],
    "answer": "7"
  },
  {
    "question": "Apa nama proses di mana tumbuhan membuat makanannya sendiri menggunakan sinar matahari?",
    "options": ["Respirasi", "Transpirasi", "Fotosintesis", "Penyerbukan"],
    "answer": "Fotosintesis"
  },
  {
    "question": "Pulau terbesar di Indonesia adalah?",
    "options": ["Jawa", "Sulawesi", "Papua", "Kalimantan"],
    "answer": "Papua"
  },
  {
    "question": "Alat musik gesek yang paling umum adalah?",
    "options": ["Gitar", "Piano", "Biola", "Drum"],
    "answer": "Biola"
  },
  {
    "question": "Pada tahun berapakah Candi Borobudur selesai dibangun? (Perkiraan era Dinasti Syailendra)",
    "options": ["Abad ke-7", "Abad ke-8 atau 9", "Abad ke-10", "Abad ke-12"],
    "answer": "Abad ke-8 atau 9"
  },
  {
    "question": "Siapakah penemu gravitasi?",
    "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Stephen Hawking"],
    "answer": "Isaac Newton"
  },
  {
    "question": "Apakah negara dengan jumlah penduduk terbanyak di dunia?",
    "options": ["India", "China", "Amerika Serikat", "Indonesia"],
    "answer": "China"
  },
  {
    "question": "Bahan bakar fosil utama yang digunakan untuk menghasilkan listrik adalah?",
    "options": ["Minyak Bumi", "Gas Alam", "Batu Bara", "Energi Surya"],
    "answer": "Batu Bara"
  },
  {
    "question": "Apakah nama ibu kota negara Thailand?",
    "options": ["Hanoi", "Kuala Lumpur", "Singapura", "Bangkok"],
    "answer": "Bangkok"
  },
  {
    "question": "Sistem penulisan kuno yang digunakan oleh Mesir kuno adalah?",
    "options": ["Alfabet Latin", "Huruf Kanji", "Hieroglif", "Aksara Jawa"],
    "answer": "Hieroglif"
  },
  {
    "question": "Cabang ilmu pengetahuan yang mempelajari kehidupan adalah?",
    "options": ["Fisika", "Kimia", "Geologi", "Biologi"],
    "answer": "Biologi"
  },
  {
    "question": "Danau terbesar di dunia (berdasarkan luas permukaan) adalah?",
    "options": ["Danau Superior", "Danau Huron", "Danau Victoria", "Laut Kaspia"],
    "answer": "Laut Kaspia"
  },
  {
    "question": "Siapakah komposer musik klasik terkenal yang tuli?",
    "options": ["Wolfgang Amadeus Mozart", "Johann Sebastian Bach", "Ludwig van Beethoven", "Joseph Haydn"],
    "answer": "Ludwig van Beethoven"
  },
  {
    "question": "Dalam permainan catur, bidak manakah yang hanya bisa bergerak secara diagonal?",
    "options": ["Benteng", "Kuda", "Raja", "Gajah"],
    "answer": "Gajah"
  },
  {
    "question": "Apa nama molekul yang menyimpan informasi genetik dalam sel?",
    "options": ["RNA", "Protein", "DNA", "Karbohidrat"],
    "answer": "DNA"
  },
  {
    "question": "Gurun terluas di dunia (gurun panas) adalah?",
    "options": ["Gurun Gobi", "Gurun Kalahari", "Gurun Sahara", "Gurun Arab"],
    "answer": "Gurun Sahara"
  },
  {
    "question": "Apakah nama satuan pengukuran suhu dalam sistem internasional (SI)?",
    "options": ["Celsius", "Fahrenheit", "Kelvin", "Reamur"],
    "answer": "Kelvin"
  },
  {
    "question": "Siapakah tokoh dongeng yang dikenal dengan hidung yang memanjang saat berbohong?",
    "options": ["Cinderella", "Peter Pan", "Pinokio", "Alice"],
    "answer": "Pinokio"
  },
  {
    "question": "Pada tahun berapakah Piala Dunia pertama kali diselenggarakan?",
    "options": ["1926", "1928", "1930", "1934"],
    "answer": "1930"
  },
  {
    "question": "Apa nama proses perubahan wujud dari cair menjadi gas?",
    "options": ["Meleleh", "Membeku", "Menguap", "Mengembun"],
    "answer": "Menguap"
  },
  {
    "question": "Apakah ibu kota negara Jerman?",
    "options": ["Munich", "Berlin", "Hamburg", "Frankfurt"],
    "answer": "Berlin"
  },
  {
    "question": "Pahlawan nasional Indonesia yang dijuluki \"Bapak Pendidikan Nasional\" adalah?",
    "options": ["Soekarno", "Mohammad Hatta", "Jenderal Sudirman", "Ki Hajar Dewantara"],
    "answer": "Ki Hajar Dewantara"
  },
  {
    "question": "Planet manakah yang dikenal sebagai \"Planet Merah\"?",
    "options": ["Venus", "Bumi", "Mars", "Jupiter"],
    "answer": "Mars"
  },
  {
    "question": "Unsur kimia apakah yang paling melimpah di kerak Bumi?",
    "options": ["Besi", "Aluminium", "Oksigen", "Silikon"],
    "answer": "Oksigen"
  },
  {
    "question": "Siapakah pengarang buku \"Perahu Kertas\"?",
    "options": ["Andrea Hirata", "Tere Liye", "Dee Lestari", "Pramoedya Ananta Toer"],
    "answer": "Dee Lestari"
  },
  {
    "question": "Gunung api tertinggi di Indonesia adalah?",
    "options": ["Gunung Semeru", "Gunung Rinjani", "Gunung Merapi", "Puncak Jaya"],
    "answer": "Puncak Jaya"
  },
  {
    "question": "Alat ukur apakah yang digunakan untuk mengukur tekanan udara?",
    "options": ["Termometer", "Anemometer", "Barometer", "Higrometer"],
    "answer": "Barometer"
  },
  {
    "question": "Siapakah sutradara film \"Parasite\" yang memenangkan Best Picture Oscar 2020?",
    "options": ["Christopher Nolan", "Quentin Tarantino", "Bong Joon-ho", "jack kichen"],
    "answer": "Bong Joon-ho"
  },
  {
    "question": "Cabang olahraga renang yang berenang telentang adalah?",
    "options": ["Gaya Bebas", "Gaya Dada", "Gaya Kupu-kupu", "Gaya Punggung"],
    "answer": "Gaya Punggung"
  },
  {
    "question": "Berapakah jumlah kromosom pada sel tubuh manusia normal?",
    "options": ["23", "45", "46", "48"],
    "answer": "46"
  },
  {
    "question": "Negara manakah yang dikenal dengan \"Kota Terlarang\" (Forbidden City)?",
    "options": ["Jepang", "Korea Selatan", "China", "Vietnam"],
    "answer": "China"
  },
  {
    "question": "Apakah nama peristiwa penting pada tahun 1928 yang melahirkan sumpah persatuan pemuda Indonesia?",
    "options": ["Hari Pendidikan Nasional", "Hari Pahlawan", "Proklamasi Kemerdekaan", "Sumpah Pemuda"],
    "answer": "Sumpah Pemuda"
  },
  {
    "question": "Benda langit apakah yang merupakan bola gas panas yang memancarkan cahaya?",
    "options": ["Bintang", "Planet", "Bulan", "Asteroid"],
    "answer": "Bintang"
  },
  {
    "question": "Apakah rumus kimia untuk karbon dioksida?",
    "options": ["H2O", "O2", "CO2", "N2"],
    "answer": "CO2"
  },
  {
    "question": "Siapakah pelukis terkenal yang memotong telinganya sendiri?",
    "options": ["Claude Monet", "Pablo Picasso", "Vincent van Gogh", "Salvador Dalí"],
    "answer": "Vincent van Gogh"
  },
  {
    "question": "Olahraga apakah yang dimainkan dengan raket dan shuttlecock?",
    "options": ["Tenis", "Tenis Meja", "Bulu Tangkis", "Squash"],
    "answer": "Bulu Tangkis"
  },
  {
    "question": "Apakah nama organ tubuh yang berfungsi menyaring darah dan menghasilkan urin?",
    "options": ["Hati", "Lambung", "Ginjal", "Limpa"],
    "answer": "Ginjal"
  },
  {
    "question": "Benua manakah yang seluruh wilayahnya terletak di belahan Bumi selatan?",
    "options": ["Afrika", "Amerika Selatan", "Asia", "Australia"],
    "answer": "Australia"
  },
  {
    "question": "Mata uang negara Inggris adalah?",
    "options": ["Euro", "Pound Sterling", "Dollar", "Yen"],
    "answer": "Pound Sterling"
  },
  {
    "question": "Siapakah penemu penisilin?",
    "options": ["Louis Pasteur", "Robert Koch", "Joseph Lister", "Alexander Fleming"],
    "answer": "Alexander Fleming"
  },
  {
    "question": "Bahasa nasional negara Brasil adalah?",
    "options": ["Spanyol", "Inggris", "Prancis", "Portugis"],
    "answer": "Portugis"
  },
  {
    "question": "Pada tahun berapakah Tembok Berlin runtuh?",
    "options": ["1985", "1987", "1989", "1991"],
    "answer": "1989"
  },
  {
    "question": "Apakah nama lapisan terluar Bumi?",
    "options": ["Mantel", "Inti Bumi", "Kerak Bumi", "Litosfer"],
    "answer": "Kerak Bumi"
  },
  {
    "question": "Siapakah tokoh mitologi Yunani yang terkenal kuat dan memiliki 12 tugas heroik?",
    "options": ["Achilles", "Odysseus", "Heracles (Hercules)", "Perseus"],
    "answer": "Heracles (Hercules)"
  },
  {
    "question": "Olahraga apakah yang menggunakan istilah \"hole-in-one\"?",
    "options": ["Basket", "Baseball", "Golf", "Tenis"],
    "answer": "Golf"
  },
  {
    "question": "Apakah nama gas yang kita hirup untuk bernapas?",
    "options": ["Karbon Dioksida", "Nitrogen", "Oksigen", "Hidrogen"],
    "answer": "Oksigen"
  },
  {
    "question": "Ibu kota provinsi Jawa Barat adalah?",
    "options": ["Surabaya", "Semarang", "Bandung", "Yogyakarta"],
    "answer": "Bandung"
  },
  {
    "question": "Siapakah penemu roda?",
    "options": ["Leonardo da Vinci", "Thomas Edison", "Tidak diketahui (penemuan prasejarah)", "Archimedes"],
    "answer": "Tidak diketahui (penemuan prasejarah)"
  },
  {
    "question": "Lautan apakah yang terletak di antara Asia dan Afrika?",
    "options": ["Atlantik", "Pasifik", "Hindia", "Arktik"],
    "answer": "Hindia"
  },
  {
    "question": "Apakah nama tarian tradisional dari Sumatera Barat yang menggunakan piring?",
    "options": ["Tari Saman", "Tari Kecak", "Tari Jaipong", "Tari Piring"],
    "answer": "Tari Piring"
  },
  {
    "question": "Berapakah jumlah hari dalam satu tahun kabisat?",
    "options": ["365", "366", "364", "367"],
    "answer": "366"
  },
  {
    "question": "Apa nama energi yang dihasilkan oleh pergerakan air?",
    "options": ["Energi Surya", "Energi Angin", "Energi Hidro", "Energi Panas Bumi"],
    "answer": "Energi Hidro"
  },
  {
    "question": "Negara kepulauan terbesar di dunia adalah?",
    "options": ["Filipina", " Jepang", "Indonesia", "Maladewa"],
    "answer": "Indonesia"
  },
  {
    "question": "Siapakah penulis novel \"Ayat-Ayat Cinta\"?",
    "options": ["Andrea Hirata", "Habiburrahman El Shirazy", "Tere Liye", "Asma Nadia"],
    "answer": "Habiburrahman El Shirazy"
  },
  {
    "question": "Olahraga apakah yang menggunakan net dan bola yang dipukul melintasi net?",
    "options": ["Sepak Bola", "Basket", "Baseball", "Voli"],
    "answer": "Voli"
  },
  {
    "question": "Apakah nama zat padat yang terbentuk secara alami dengan struktur kristal?",
    "options": ["Batuan", "Mineral", "Tanah", "Fosil"],
    "answer": "Mineral"
  },
  {
    "question": "Gurun manakah yang terletak di Antartika?",
    "options": ["Gurun Sahara", "Gurun Gobi", "Gurun Pasir", "Gurun Antartika"],
    "answer": "Gurun Antartika"
  },
  {
    "question": "Alat musik tiup yang terbuat dari logam dan dimainkan dengan menggunakan katup adalah?",
    "options": ["Seruling", "Klarinet", "Terompet", "Saksofon"],
    "answer": "Terompet"
  },
  {
    "question": "Siapakah penjelajah yang pertama kali menginjakkan kaki di bulan?",
    "options": ["Buzz Aldrin", "Michael Collins", "Yuri Gagarin", "Neil Armstrong"],
    "answer": "Neil Armstrong"
  },
  {
    "question": "Apakah nama galaksi tempat tata surya kita berada?",
    "options": ["Andromeda", "Triangulum", "Bima Sakti (Milky Way)", "Centaurus A"],
    "answer": "Bima Sakti (Milky Way)"
  }
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