import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import CartItem from "../components/CartItem";
import CartSummary from "../components/CartSummary";
import EmptyState from "../components/EmptyState";
import client from "../api/client";

export default function Checkout() {
  const { items, removeItem, updateQuantity, total, clearCart } = useCart();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleConfirm() {
    if (items.length === 0) return;
    setSubmitting(true);
    setError(null);

    try {
      // We only send { menu_item_id, quantity } — never a price or total.
      // The backend looks up the real price and computes the total itself,
      // so a tampered request body can't change what gets charged.
      const payload = {
        items: items.map((i) => ({ menu_item_id: i.id, quantity: i.quantity })),
      };
      const res = await client.post("/orders", payload);
      clearCart();
      navigate("/order-success", { state: { order: res.data } });
    } catch {
      setError("Couldn't place the order. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (items.length === 0) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-10">
        <EmptyState message="Your cart is empty. Add something from the menu first." />
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-semibold text-neutral-900 mb-4">
        Your Order
      </h1>

      <div className="space-y-3">
        {items.map((item) => (
          <CartItem
            key={item.id}
            item={item}
            onRemove={() => removeItem(item.id)}
            onQuantityChange={(q) => updateQuantity(item.id, q)}
          />
        ))}
      </div>

      <CartSummary total={total} />

      {error && <p className="text-red-600 mt-3 text-sm">{error}</p>}

      <button
        onClick={handleConfirm}
        disabled={submitting}
        className="mt-6 w-full py-3 rounded-xl bg-neutral-900 text-white font-medium hover:bg-neutral-700 transition-colors disabled:opacity-50"
      >
        {submitting ? "Placing order..." : "Confirm Order"}
      </button>
    </div>
  );
}
