import numpy as np
import plotly.graph_objects as go

# ===============================
# Part 1 — Real secp256k1 curve
# ===============================
x_min = -np.cbrt(7)  # domain start ≈ -1.912931
x_max = 4.0

x = np.linspace(x_min, x_max, 2000)
rad = x ** 3 + 7
mask = rad >= 0
y = np.sqrt(np.clip(rad, 0, None))
yn = -y

fig = go.Figure()
fig.add_trace(go.Scatter(x=x[mask], y=y[mask], mode="lines", name="y = +√(x³ + 7)"))
fig.add_trace(go.Scatter(x=x[mask], y=yn[mask], mode="lines", name="y = -√(x³ + 7)"))
fig.update_layout(title="EC secp256k1 over ℝ:  y² = x³ + 7", xaxis_title="x", yaxis_title="y")
fig.update_yaxes(scaleanchor=None, scaleratio=1, range=[-9, 9])
fig.update_xaxes(range=[-2, 4])
fig.add_vline(x=x_min, line_dash="dot")

with open("secp256k1_real.html", "w") as f:
    f.write(fig.to_html())


# =========================================
# Helpers for finite-field (mod p) plotting
# =========================================
def legendre_symbol(a, p):
    """Return 1 if a is a quadratic residue mod p, -1 if non-residue, 0 if a==0."""
    a %= p
    if a == 0:
        return 0
    return pow(a, (p - 1) // 2, p) if pow(a, (p - 1) // 2, p) in (0, 1) else -1


def tonelli_shanks(n, p):
    """Solve y^2 ≡ n (mod p) for odd prime p. Return a solution y or None if no root."""
    assert p % 2 == 1
    n %= p
    if n == 0:
        return 0
    # simple case p % 4 == 3
    if p % 4 == 3:
        y = pow(n, (p + 1) // 4, p)
        if (y * y) % p == n:
            return y
        return None
    # Tonelli–Shanks general case
    # write p-1 = Q * 2^S with Q odd
    Q, S = p - 1, 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    # find z a non-residue
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)
    while True:
        if t == 0:
            return 0
        if t == 1:
            return R
        # find least i (0<i<M) with t^(2^i) == 1
        i, t2i = 1, (t * t) % p
        while i < M and t2i != 1:
            t2i = (t2i * t2i) % p
            i += 1
        if i == M:  # no solution
            return None
        b = pow(c, 1 << (M - i - 1), p)
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p


def ec_points_slice(a, b, p, x_start=0, x_count=5000):
    """Collect points (x,y) on y^2 = x^3 + a x + b (mod p) for x in [x_start, x_start+x_count)."""
    xs, ys = [], []
    for x in range(x_start, x_start + x_count):
        rhs = (pow(x, 3, p) + a * x + b) % p
        ls = pow(rhs, (p - 1) // 2, p)  # Legendre symbol via Euler's criterion
        if ls == p - 1:  # non-residue
            continue
        if rhs == 0:
            y = 0
            xs.append(x);
            ys.append(y)
            continue
        y = tonelli_shanks(rhs, p)
        if y is None:
            continue
        xs.append(x);
        ys.append(y)
        y2 = (-y) % p
        if y2 != y:
            xs.append(x);
            ys.append(y2)
    return xs, ys


# =======================================================
# Part 2a — Small prime demo: plot ALL finite-field points
# =======================================================
p_small = 97
a_small, b_small = 0, 7
xs_all, ys_all = [], []
for x in range(p_small):
    rhs = (pow(x, 3, p_small) + a_small * x + b_small) % p_small
    if rhs == 0:
        xs_all.append(x);
        ys_all.append(0)
        continue
    y = tonelli_shanks(rhs, p_small)
    if y is None:
        continue
    xs_all += [x, x]
    ys_all += [y, (-y) % p_small]

fig_small = go.Figure()
fig_small.add_trace(go.Scatter(x=xs_all, y=ys_all, mode="markers",
                               marker=dict(size=6),
                               name=f"All points mod {p_small}"))
fig_small.update_layout(title=f"secp256k1 mod {p_small}: y² = x³ + 7 (all points)",
                        xaxis_title="x (mod p)", yaxis_title="y (mod p)")
with open("secp256k1_mod_p_small.html", "w") as f:
    f.write(fig_small.to_html())

# --- replace your Part 2b (true secp256k1) with this ---

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # secp256k1 prime
a, b = 0, 7

def ec_points_slice(a, b, p, x_start=0, x_count=6000):
    xs, ys = [], []
    for x in range(x_start, x_start + x_count):
        rhs = (pow(x, 3, p) + a * x + b) % p
        # Euler's criterion: if rhs^((p-1)/2) == p-1 → non-residue (no sqrt)
        if pow(rhs, (p - 1) // 2, p) == p - 1:
            continue
        # Tonelli–Shanks for modular sqrt
        y = tonelli_shanks(rhs, p)
        if y is None:
            continue
        xs.append(x); ys.append(y)
        y2 = (-y) % p
        if y2 != y:
            xs.append(x); ys.append(y2)
    return xs, ys

# get a slice of points (as Python ints)
X_START, X_MAX = 0, 6000
xs, ys = ec_points_slice(a, b, p, x_start=X_START, x_count=X_MAX)

# SCALE to floats that Plotly can serialize:
#   - x_scaled in [0,1] within the sampled window
#   - y_scaled in [0,1] by dividing by p
x_scaled = [(x - X_START) / float(X_MAX) for x in xs]
y_scaled = [y / float(p) for y in ys]

fig_mod = go.Figure()
fig_mod.add_trace(go.Scatter(
    x=x_scaled, y=y_scaled, mode="markers",
    marker=dict(size=2),
    name=f"secp256k1 points (x∈[{X_START},{X_START+X_MAX})) scaled"
))
fig_mod.update_layout(
    title="secp256k1 over 𝔽_p (scaled view of a small x-slice)",
    xaxis_title="x (scaled within slice)", yaxis_title="y / p (0..1)"
)
with open("secp256k1_mod_p_slice_scaled.html", "w") as f:
    f.write(fig_mod.to_html())

print("Wrote: secp256k1_real.html, secp256k1_mod_p_small.html, secp256k1_mod_p_slice.html")
