function loginWallet() {
  const privateKey = document.getElementById('login-private').value.trim();
  if (!privateKey) return alert('Please enter your private key');

  // Simpan private key di localStorage untuk validasi selanjutnya
  localStorage.setItem('comcoin_private_key', privateKey);

  // Validasi private key dengan memanggil backend
  fetch('http://localhost:5000/get_public_key', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ private_key: privateKey }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.public_key) {
        document.getElementById('auth-section').classList.add('hidden');
        document.getElementById('wallet-section').classList.remove('hidden');
        document.getElementById('wallet-public').value = data.public_key;
        loadWalletData(data.public_key);
      } else {
        alert('Invalid private key');
      }
    })
    .catch((err) => {
      alert('Error: ' + err);
    });
}

function loadWalletData(publicKey) {
  // Dapatkan saldo
  fetch('http://localhost:5000/get_balance', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ public_key: publicKey }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('wallet-balance').textContent =
        'Balance: ' + data.balance + ' ComCoin';
    });

  // Dapatkan histori transaksi
  fetch('http://localhost:5000/get_transactions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ public_key: publicKey }),
  })
    .then((response) => response.json())
    .then((data) => {
      const transactionList = document.getElementById('transaction-list');
      transactionList.innerHTML = '';
      data.transactions.forEach((tx) => {
        const listItem = document.createElement('li');
        listItem.textContent = `${tx.sender} sent ${tx.amount} to ${tx.recipient}`;
        transactionList.appendChild(listItem);
      });
    });
}

function sendTransaction() {
  const recipient = document.getElementById('recipient').value;
  const amount = document.getElementById('amount').value;
  const privateKey = localStorage.getItem('comcoin_private_key');

  if (!recipient || !amount || !privateKey) {
    return alert('Please fill all fields');
  }

  // Sign transaction with private key
  fetch('http://localhost:5000/get_public_key', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ private_key: privateKey }),
  })
    .then((response) => response.json())
    .then((data) => {
      const tx = {
        sender: data.public_key,
        recipient: recipient,
        amount: parseFloat(amount),
        signature: null, // We can later add digital signing
      };
      fetch('http://localhost:5000/new_transaction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tx),
      }).then(() => {
        alert('Transaction sent!');
        loadWalletData(data.public_key); // Refresh data
      });
    });
}
