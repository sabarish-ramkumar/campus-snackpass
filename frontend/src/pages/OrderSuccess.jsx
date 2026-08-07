import { useLocation, Link } from "react-router-dom";

export default function OrderSuccess() {
  const location = useLocation();
  const order = location.state?.order;

  // If someone lands here directly (refresh, back button, shared link)
  // there's no order in navigation state — send them back gracefully
  // instead of showing a broken page.
  if (!order) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center">
        <p className="text-neutral-600">No recent order found.</p>
        <Link to="/" className="text-neutral-900 underline mt-2 inline-block">
          Back to menu
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto px-4 py-16 text-center">
      <h1 className="text-xl font-medium text-neutral-900 mb-2">
        Order confirmed!
      </h1>
      <p className="text-neutral-500 mb-6">
        Show this token at the counter to collect your food.
      </p>

      <div className="text-4xl font-bold tracking-widest bg-neutral-100 rounded-2xl py-8 mb-6 text-neutral-900">
        {order.token}
      </div>

      <p className="text-neutral-600 mb-8">
        Total paid: ₹{order.total.toFixed(2)}
      </p>

      <Link
        to="/"
        className="inline-block px-6 py-3 rounded-xl bg-neutral-900 text-white font-medium hover:bg-neutral-700 transition-colors"
      >
        Order more
      </Link>
    </div>
  );
}
