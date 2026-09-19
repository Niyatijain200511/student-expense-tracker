// ---------- Data ----------
// Same idea as your Python "transactions = []" list of dictionaries
let transactions = [];
let monthlyBudget = 0;

const STORAGE_KEY = "student_expense_tracker_data";

// ---------- Persistence (like Python's json.load / json.dump) ----------
function loadData() {
  let saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    let data = JSON.parse(saved);
    transactions = data.transactions || [];
    monthlyBudget = data.monthlyBudget || 0;
  }
}

function saveData() {
  let data = { transactions: transactions, monthlyBudget: monthlyBudget };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

// ---------- UI helpers ----------
function toggleCategoryField() {
  let type = document.getElementById("typeSelect").value;
  document.getElementById("categoryWrapper").style.display =
    type === "expense" ? "block" : "none";
}

// ---------- Add transaction ----------
function addTransaction() {
  let type = document.getElementById("typeSelect").value;
  let amountText = document.getElementById("amountInput").value;
  let amount = parseFloat(amountText);
  let dateValue = document.getElementById("dateInput").value;

  if (isNaN(amount) || amount <= 0) {
    alert("Please enter a valid amount greater than zero.");
    return;
  }

  let category = type === "expense"
    ? document.getElementById("categorySelect").value
    : "Income";

  let date = dateValue ? dateValue : new Date().toISOString().split("T")[0];

  let transaction = {
    id: Date.now(),
    type: type,
    amount: amount,
    category: category,
    date: date
  };

  transactions.push(transaction);
  saveData();

  document.getElementById("amountInput").value = "";

  renderTransactions();
  renderSummary();
  renderCategoryReport();
  checkBudgetWarning();
}

// ---------- Delete transaction ----------
function deleteTransaction(id) {
  transactions = transactions.filter(t => t.id !== id);
  saveData();
  renderTransactions();
  renderSummary();
  renderCategoryReport();
  checkBudgetWarning();
}

// ---------- Search / filter ----------
function getFilteredTransactions() {
  let query = document.getElementById("searchInput").value.trim().toLowerCase();
  if (!query) return transactions;

  return transactions.filter(t =>
    t.category.toLowerCase().includes(query) ||
    t.type.toLowerCase().includes(query) ||
    t.date.includes(query)
  );
}

// ---------- Calculations ----------
function calculateTotal(type) {
  return transactions
    .filter(t => t.type === type)
    .reduce((sum, t) => sum + t.amount, 0);
}

function calculateBalance() {
  return calculateTotal("income") - calculateTotal("expense");
}

function calculateCategoryTotals() {
  let totals = {};
  transactions.forEach(t => {
    if (t.type === "expense") {
      totals[t.category] = (totals[t.category] || 0) + t.amount;
    }
  });
  return totals;
}

// ---------- Budget ----------
function setBudget() {
  let value = parseFloat(document.getElementById("budgetInput").value);
  if (isNaN(value) || value <= 0) {
    alert("Please enter a valid budget amount.");
    return;
  }
  monthlyBudget = value;
  saveData();
  checkBudgetWarning();
  alert("Monthly budget saved!");
}

function checkBudgetWarning() {
  let warningEl = document.getElementById("budgetWarning");
  let totalExpense = calculateTotal("expense");

  if (monthlyBudget <= 0) {
    warningEl.textContent = "";
    return;
  }

  if (totalExpense > monthlyBudget) {
    warningEl.textContent = "⚠ You have exceeded your monthly budget of ₹" + monthlyBudget.toFixed(2) + "!";
  } else if (totalExpense > monthlyBudget * 0.8) {
    warningEl.textContent = "⚠ You have used over 80% of your monthly budget.";
  } else {
    warningEl.textContent = "";
  }
}

// ---------- Rendering ----------
function renderTransactions() {
  let list = document.getElementById("transactionList");
  list.innerHTML = "";

  let data = getFilteredTransactions();

  if (data.length === 0) {
    list.innerHTML = "<li>No transactions found.</li>";
    return;
  }

  data.forEach(t => {
    let li = document.createElement("li");

    let label = document.createElement("span");
    let sign = t.type === "income" ? "+" : "−";
    label.textContent = `${t.date} — ${t.category}: ${sign}₹${t.amount.toFixed(2)}`;
    label.className = t.type === "income" ? "income-text" : "expense-text";

    let delBtn = document.createElement("button");
    delBtn.textContent = "Delete";
    delBtn.className = "delete-btn";
    delBtn.onclick = function () { deleteTransaction(t.id); };

    li.appendChild(label);
    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

function renderSummary() {
  document.getElementById("totalIncomeDisplay").textContent =
    "Total income: ₹" + calculateTotal("income").toFixed(2);
  document.getElementById("totalExpenseDisplay").textContent =
    "Total expenses: ₹" + calculateTotal("expense").toFixed(2);
  document.getElementById("balanceDisplay").textContent =
    "Balance: ₹" + calculateBalance().toFixed(2);
}

function renderCategoryReport() {
  let reportEl = document.getElementById("categoryReport");
  reportEl.innerHTML = "";

  let totals = calculateCategoryTotals();
  let categories = Object.keys(totals);

  if (categories.length === 0) {
    reportEl.innerHTML = "<li>No expenses recorded yet.</li>";
    return;
  }

  categories.forEach(cat => {
    let li = document.createElement("li");
    li.innerHTML = `<span>${cat}</span><span>₹${totals[cat].toFixed(2)}</span>`;
    reportEl.appendChild(li);
  });
}

// ---------- CSV Export ----------
function exportToCSV() {
  if (transactions.length === 0) {
    alert("No transactions to export.");
    return;
  }

  let rows = [["Type", "Category", "Amount", "Date"]];
  transactions.forEach(t => {
    rows.push([t.type, t.category, t.amount, t.date]);
  });

  let csvContent = rows.map(row => row.join(",")).join("\n");

  let blob = new Blob([csvContent], { type: "text/csv" });
  let url = URL.createObjectURL(blob);

  let a = document.createElement("a");
  a.href = url;
  a.download = "transactions.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ---------- Init ----------
function init() {
  loadData();
  document.getElementById("dateInput").value = new Date().toISOString().split("T")[0];
  document.getElementById("budgetInput").value = monthlyBudget || "";
  toggleCategoryField();
  renderTransactions();
  renderSummary();
  renderCategoryReport();
  checkBudgetWarning();
}

init();