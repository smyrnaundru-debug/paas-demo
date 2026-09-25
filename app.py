import os
from flask import Flask, request, render_template_string, redirect, session

app = Flask(__name__)
# Secret key for login sessions
app.secret_key = os.environ.get("SECRET_KEY", "saas-demo-secret-key")

# ============================================================
# USER LOGIN DATA
# ============================================================
USERS = {
    "alpha": {
        "password": "alpha123",
        "company": "Company Alpha"
    },
    "beta": {
        "password": "beta123",
        "company": "Company Beta"
    }
}

# ============================================================
# SaaS DATA
# ============================================================
DATA = {
    "Company Alpha": {
        "revenue": 45000,
        "users": 120,
        "orders": 326,
        "growth": 18.5,
        "customers": [
            ("ABC Technologies", "IT", "Active"),
            ("Global Systems", "Finance", "Active"),
            ("Future Tech", "Marketing", "Active"),
            ("Smart Solutions", "HR", "Inactive")
        ],
        "order_list": [
            ("ORD-1001", "ABC Technologies", "$4,500", "Paid"),
            ("ORD-1002", "Global Systems", "$3,200", "Paid"),
            ("ORD-1003", "Future Tech", "$2,850", "Pending"),
            ("ORD-1004", "Smart Solutions", "$5,100", "Paid")
        ],
        "monthly": [20, 28, 25, 32, 38, 41, 45]
    },
    "Company Beta": {
        "revenue": 120000,
        "users": 280,
        "orders": 815,
        "growth": 27.4,
        "customers": [
            ("Alpha Industries", "IT", "Active"),
            ("Tech World", "Marketing", "Active"),
            ("Digital Corp", "Finance", "Active"),
            ("Enterprise Ltd", "HR", "Active")
        ],
        "order_list": [
            ("ORD-2001", "Alpha Industries", "$8,200", "Paid"),
            ("ORD-2002", "Tech World", "$12,500", "Paid"),
            ("ORD-2003", "Digital Corp", "$6,750", "Pending"),
            ("ORD-2004", "Enterprise Ltd", "$15,300", "Paid")
        ],
        "monthly": [35, 48, 55, 72, 85, 100, 120]
    }
}

# ============================================================
# LOGIN PAGE
# ============================================================
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>SaaSCloud Login</title>
<style>
body {
    margin: 0;
    font-family: Arial;
    background: #f1f5f9;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.login {
    background: white;
    width: 360px;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 5px 20px #ccc;
}
.logo {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
    margin-bottom: 30px;
}
input {
    width: 100%;
    padding: 13px;
    margin: 8px 0 18px 0;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    box-sizing: border-box;
    font-size: 15px;
}
button {
    width: 100%;
    padding: 13px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 7px;
    font-size: 16px;
    cursor: pointer;
}
button:hover {
    background: #1d4ed8;
}
.error {
    color: #dc2626;
    text-align: center;
    margin-bottom: 15px;
}
.demo {
    margin-top: 25px;
    background: #f8fafc;
    padding: 15px;
    border-radius: 8px;
    font-size: 13px;
}
</style>
</head>
<body>
<div class="login">
    <div class="logo">
    ☁ SaaSCloud
    </div>
    <h2>Sign In</h2>
    <p>Access your SaaS dashboard</p>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
    <form method="post">
    <label>Username</label>
    <input
    type="text"
    name="username"
    required
    >
    <label>Password</label>
    <input
    type="password"
    name="password"
    required
    >
    <button type="submit">
    Login
    </button>
    </form>
    <div class="demo">
    <b>Demo Accounts</b><br><br>
    Alpha → alpha / alpha123<br>
    Beta → beta / beta123
    </div>
</div>
</body>
</html>
"""

# ============================================================
# LOGIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username]["password"] == password:
            session["username"] = username
            session["company"] = USERS[username]["company"]
            return redirect("/")
        return render_template_string(
            LOGIN_PAGE,
            error="Invalid username or password"
        )
    return render_template_string(
        LOGIN_PAGE,
        error=None
    )

# ============================================================
# LOGOUT
# ============================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ============================================================
# CHECK LOGIN
# ============================================================
def logged_in():
    return "username" in session

# ============================================================
# COMMON DASHBOARD DESIGN
# ============================================================
PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>SaaSCloud</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {
    margin: 0;
    font-family: Arial;
    background: #f4f7fb;
    color: #172033;
}
/* SIDEBAR */
.sidebar {
    position: fixed;
    width: 220px;
    height: 100vh;
    background: #111827;
    color: white;
    padding: 25px;
}
.logo {
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 40px;
}
.menu {
    display: block;
    color: white;
    text-decoration: none;
    padding: 14px;
    margin: 8px 0;
    border-radius: 8px;
}
.menu:hover,
.active {
    background: #2563eb;
}
.logout {
    margin-top: 40px;
}
/* MAIN */
.main {
    margin-left: 270px;
    padding: 30px;
}
/* HEADER */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.header h1 {
    margin: 0;
    font-size: 32px;
}
.header p {
    color: #64748b;
}
/* COMPANY */
.company {
    background: #e0ecff;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: bold;
}
/* CARDS */
.cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
}
.card {
    background: white;
    padding: 22px;
    border-radius: 12px;
    box-shadow: 0 3px 10px #ddd;
}
.card h3 {
    color: #64748b;
    font-size: 15px;
}
.value {
    font-size: 28px;
    font-weight: bold;
}
.green {
    color: #16a34a;
}
/* BOX */
.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
    margin-top: 20px;
    box-shadow: 0 3px 10px #ddd;
}
/* TABLE */
table {
    width: 100%;
    border-collapse: collapse;
}
th,
td {
    padding: 14px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}
th {
    color: #64748b;
}
.paid {
    color: #16a34a;
    font-weight: bold;
}
.pending {
    color: #d97706;
    font-weight: bold;
}
/* CHART */
.chart {
    height: 350px;
}
</style>
</head>
<body>
<!-- SIDEBAR -->
<div class="sidebar">
    <div class="logo">
    ☁ SaaSCloud
    </div>
    <a class="menu {% if page == 'Dashboard' %}active{% endif %}" href="/">
    Dashboard
    </a>
    <a class="menu {% if page == 'Analytics' %}active{% endif %}" href="/analytics">
    Analytics
    </a>
    <a class="menu {% if page == 'Customers' %}active{% endif %}" href="/customers">
    Customers
    </a>
    <a class="menu {% if page == 'Orders' %}active{% endif %}" href="/orders">
    Orders
    </a>
    <a class="menu {% if page == 'Reports' %}active{% endif %}" href="/reports">
    Reports
    </a>
    <a class="menu logout" href="/logout">
    Logout
    </a>
</div>
<!-- MAIN -->
<div class="main">
    <div class="header">
        <div>
            <h1>{{ page }}</h1>
            <p>SaaS Management Platform</p>
        </div>
        <div class="company">
            {{ company }}
        </div>
    </div>
    {{ content | safe }}
</div>
</body>
</html>
"""

# ============================================================
# DASHBOARD
# ============================================================
@app.route("/")
def dashboard():
    if not logged_in():
        return redirect("/login")
    company = session["company"]
    d = DATA[company]
    content = """
    <div class="cards">
        <div class="card">
            <h3>Total Revenue</h3>
            <div class="value">${{ "{:,}".format(d.revenue) }}</div>
            <p class="green">↑ {{ d.growth }}%</p>
        </div>
        <div class="card">
            <h3>Active Users</h3>
            <div class="value">{{ d.users }}</div>
            <p class="green">↑ 12.8%</p>
        </div>
        <div class="card">
            <h3>Total Orders</h3>
            <div class="value">{{ d.orders }}</div>
            <p class="green">↑ 9.4%</p>
        </div>
        <div class="card">
            <h3>Customer Growth</h3>
            <div class="value">{{ d.growth }}%</div>
            <p class="green">Positive growth</p>
        </div>
    </div>
    <div class="box">
        <h2>Revenue Overview</h2>
        <div class="chart">
            <canvas id="revenueChart"></canvas>
        </div>
    </div>
    <div class="box">
        <h2>Recent Orders</h2>
        <table>
            <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Amount</th>
                <th>Status</th>
            </tr>
            {% for order in d.order_list %}
            <tr>
                <td>{{ order[0] }}</td>
                <td>{{ order[1] }}</td>
                <td>{{ order[2] }}</td>
                <td>
                    {% if order[3] == "Paid" %}
                    <span class="paid">● Paid</span>
                    {% else %}
                    <span class="pending">● Pending</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    <script>
    new Chart(
        document.getElementById("revenueChart"),
        {
            type: "line",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                datasets: [{
                    label: "Revenue ($000)",
                    data: {{ d.monthly | tojson }},
                    borderWidth: 3,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        }
    );
    </script>
    """
    return render_template_string(
        PAGE,
        page="Dashboard",
        company=company,
        content=render_template_string(content, d=d)
    )

# ============================================================
# ANALYTICS
# ============================================================
@app.route("/analytics")
def analytics():
    if not logged_in():
        return redirect("/login")
    company = session["company"]
    d = DATA[company]
    content = """
    <div class="cards">
        <div class="card">
            <h3>Revenue</h3>
            <div class="value">${{ "{:,}".format(d.revenue) }}</div>
        </div>
        <div class="card">
            <h3>Users</h3>
            <div class="value">{{ d.users }}</div>
        </div>
        <div class="card">
            <h3>Orders</h3>
            <div class="value">{{ d.orders }}</div>
        </div>
        <div class="card">
            <h3>Growth</h3>
            <div class="value">{{ d.growth }}%</div>
        </div>
    </div>
    <div class="box">
        <h2>Monthly Revenue Analytics</h2>
        <div class="chart">
            <canvas id="analyticsChart"></canvas>
        </div>
    </div>
    <script>
    new Chart(
        document.getElementById("analyticsChart"),
        {
            type: "bar",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                datasets: [{
                    label: "Revenue ($000)",
                    data: {{ d.monthly | tojson }},
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        }
    );
    </script>
    """
    return render_template_string(
        PAGE,
        page="Analytics",
        company=company,
        content=render_template_string(content, d=d)
    )

# ============================================================
# CUSTOMERS
# ============================================================
@app.route("/customers")
def customers():
    if not logged_in():
        return redirect("/login")
    company = session["company"]
    d = DATA[company]
    content = """
    <div class="box">
        <h2>Customer Management</h2>
        <table>
            <tr>
                <th>Customer</th>
                <th>Department</th>
                <th>Status</th>
            </tr>
            {% for customer in d.customers %}
            <tr>
                <td>{{ customer[0] }}</td>
                <td>{{ customer[1] }}</td>
                <td>{{ customer[2] }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    """
    return render_template_string(
        PAGE,
        page="Customers",
        company=company,
        content=render_template_string(content, d=d)
    )

# ============================================================
# ORDERS
# ============================================================
@app.route("/orders")
def orders():
    if not logged_in():
        return redirect("/login")
    company = session["company"]
    d = DATA[company]
    content = """
    <div class="box">
        <h2>Order Management</h2>
        <table>
            <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Amount</th>
                <th>Status</th>
            </tr>
            {% for order in d.order_list %}
            <tr>
                <td>{{ order[0] }}</td>
                <td>{{ order[1] }}</td>
                <td>{{ order[2] }}</td>
                <td>
                    {% if order[3] == "Paid" %}
                    <span class="paid">● Paid</span>
                    {% else %}
                    <span class="pending">● Pending</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    """
    return render_template_string(
        PAGE,
        page="Orders",
        company=company,
        content=render_template_string(content, d=d)
    )

# ============================================================
# REPORTS
# ============================================================
@app.route("/reports")
def reports():
    if not logged_in():
        return redirect("/login")
    company = session["company"]
    d = DATA[company]
    content = """
    <div class="cards">
        <div class="card">
            <h3>Total Revenue</h3>
            <div class="value">${{ "{:,}".format(d.revenue) }}</div>
        </div>
        <div class="card">
            <h3>Customers</h3>
            <div class="value">{{ d.customers | length }}</div>
        </div>
        <div class="card">
            <h3>Orders</h3>
            <div class="value">{{ d.orders }}</div>
        </div>
        <div class="card">
            <h3>Growth</h3>
            <div class="value">{{ d.growth }}%</div>
        </div>
    </div>
    <div class="box">
        <h2>Business Report</h2>
        <p><b>Company:</b> {{ company }}</p>
        <p><b>Total Revenue:</b> ${{ "{:,}".format(d.revenue) }}</p>
        <p><b>Active Users:</b> {{ d.users }}</p>
        <p><b>Total Orders:</b> {{ d.orders }}</p>
        <p><b>Customer Growth:</b> {{ d.growth }}%</p>
        <p class="green">✓ Business performance is positive.</p>
    </div>
    """
    return render_template_string(
        PAGE,
        page="Reports",
        company=company,
        content=render_template_string(content, d=d)
    )

# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("SaaSCloud - Multi-Tenant SaaS Demo")
    print("=" * 50)
    print("Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )