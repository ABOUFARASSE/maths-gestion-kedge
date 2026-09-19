"""Fonctions de calcul testables de l'application Maths & Gestion KEDGE."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


def budget_parts(total: float, communication: float, digital: float) -> dict[str, float]:
    communication_amount = total * communication
    digital_amount = communication_amount * digital
    return {
        "communication": communication_amount,
        "digital": digital_amount,
        "communication_hors_digital": communication_amount - digital_amount,
        "reste": total - communication_amount,
    }


def future_value(initial: float, rate: float, years: int) -> float:
    return initial * (1 + rate) ** years


def linear_break_even(fixed_cost: float, price: float, variable_cost: float) -> float:
    margin = price - variable_cost
    if margin <= 0:
        raise ValueError("La marge unitaire doit être strictement positive.")
    return fixed_cost / margin


@dataclass(frozen=True)
class QuadraticResult:
    discriminant: float
    roots: tuple[float, float] | None
    vertex_x: float
    vertex_y: float


def quadratic_analysis(a: float, b: float, c: float) -> QuadraticResult:
    if a == 0:
        raise ValueError("a doit être non nul pour une fonction quadratique.")
    delta = b * b - 4 * a * c
    roots = None
    if delta >= 0:
        r1 = (-b - sqrt(delta)) / (2 * a)
        r2 = (-b + sqrt(delta)) / (2 * a)
        roots = tuple(sorted((r1, r2)))
    xv = -b / (2 * a)
    yv = a * xv**2 + b * xv + c
    return QuadraticResult(delta, roots, xv, yv)


def marginal_model(
    fixed_cost: float, a: float, b: float, price: float, demand_slope: float, q: float
) -> dict[str, float]:
    cost = fixed_cost + a * q + b * q**2
    revenue = price * q - demand_slope * q**2
    marginal_cost = a + 2 * b * q
    marginal_revenue = price - 2 * demand_slope * q
    return {
        "cost": cost,
        "revenue": revenue,
        "profit": revenue - cost,
        "marginal_cost": marginal_cost,
        "marginal_revenue": marginal_revenue,
        "marginal_profit": marginal_revenue - marginal_cost,
    }


def optimal_quantity(a: float, b: float, price: float, demand_slope: float) -> float:
    denominator = 2 * (b + demand_slope)
    if denominator <= 0:
        raise ValueError("Le modèle ne possède pas de maximum intérieur.")
    return (price - a) / denominator


def advertising_model(vmax: float, k: float, margin: float, budget: float) -> dict[str, float]:
    sales = vmax * budget / (budget + k) if budget + k else 0.0
    profit = margin * sales - budget
    marginal_sales = vmax * k / (budget + k) ** 2
    theoretical_optimum = sqrt(max(0.0, margin * vmax * k)) - k
    return {
        "sales": sales,
        "profit": profit,
        "marginal_sales": marginal_sales,
        "theoretical_optimum": max(0.0, theoretical_optimum),
    }


def integrated_product(
    demand_intercept: float,
    sensitivity: float,
    fixed_cost: float,
    variable_cost: float,
    price: float,
    capacity: float,
) -> dict[str, float]:
    demand = max(0.0, demand_intercept - sensitivity * price)
    quantity = min(demand, capacity)
    revenue = price * quantity
    cost = fixed_cost + variable_cost * quantity
    return {
        "demand": demand,
        "quantity": quantity,
        "revenue": revenue,
        "cost": cost,
        "profit": revenue - cost,
    }
