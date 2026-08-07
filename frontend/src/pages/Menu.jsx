import { useEffect, useState } from "react";
import client from "../api/client";
import MenuCard from "../components/MenuCard";
import CategoryFilter from "../components/CategoryFilter";
import SearchBar from "../components/SearchBar";
import LoadingSpinner from "../components/LoadingSpinner";
import EmptyState from "../components/EmptyState";
import { useCart } from "../context/CartContext";

export default function Menu() {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState(["All"]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { addItem } = useCart();

  // Categories are fetched once — they rarely change and aren't worth
  // re-fetching every time the filter/search state changes.
  useEffect(() => {
    client
      .get("/categories")
      .then((res) => setCategories(["All", ...res.data]))
      .catch(() => {
        // Non-critical: the "All" tab still works even if this fails.
      });
  }, []);

  // Re-fetch the menu whenever category or search changes, letting the
  // backend do the filtering (it has the full dataset; the frontend
  // should not assume it can filter a partial/local list correctly).
  useEffect(() => {
    setLoading(true);
    setError(null);

    const params = {};
    if (selectedCategory !== "All") params.category = selectedCategory;
    if (searchTerm.trim()) params.search = searchTerm.trim();

    const timeoutId = setTimeout(() => {
      client
        .get("/menu-items", { params })
        .then((res) => setItems(res.data))
        .catch(() =>
          setError("Couldn't load the menu. Is the backend running?")
        )
        .finally(() => setLoading(false));
    }, 250); // small debounce so typing doesn't fire a request per keystroke

    return () => clearTimeout(timeoutId);
  }, [selectedCategory, searchTerm]);

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-semibold text-neutral-900">
        Campus SnackPass
      </h1>
      <p className="text-neutral-500 mt-1">
        Order ahead, skip the queue, collect with your token.
      </p>

      <div className="mt-5">
        <SearchBar value={searchTerm} onChange={setSearchTerm} />
        <CategoryFilter
          categories={categories}
          selected={selectedCategory}
          onSelect={setSelectedCategory}
        />
      </div>

      {loading && <LoadingSpinner />}

      {!loading && error && (
        <p className="text-red-600 mt-8 text-center">{error}</p>
      )}

      {!loading && !error && items.length === 0 && (
        <EmptyState message="No items match your search." />
      )}

      {!loading && !error && items.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {items.map((item) => (
            <MenuCard key={item.id} item={item} onAdd={() => addItem(item)} />
          ))}
        </div>
      )}
    </div>
  );
}
