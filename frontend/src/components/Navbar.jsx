import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

export default function Navbar() {
  const { itemCount } = useCart();

  return (
    <nav className="border-b border-neutral-200 bg-white/80 backdrop-blur sticky top-0 z-10">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-semibold text-neutral-900">
          🥪 Campus SnackPass
        </Link>
        <Link
          to="/checkout"
          className="relative text-neutral-700 hover:text-neutral-900 font-medium"
        >
          Cart
          {itemCount > 0 && (
            <span className="absolute -top-2 -right-4 inline-flex items-center justify-center w-5 h-5 text-xs bg-neutral-900 text-white rounded-full">
              {itemCount}
            </span>
          )}
        </Link>
      </div>
    </nav>
  );
}
