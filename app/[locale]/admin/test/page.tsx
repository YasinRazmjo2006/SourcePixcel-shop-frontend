import { adminUsers, adminOrders, analyticsOverview, getAdminUserStats, getAdminOrderStats } from "@/lib/data";

export default function TestPage() {
  const userStats = getAdminUserStats();
  const orderStats = getAdminOrderStats();

  return (
    <div className="p-8 space-y-4">
      <h1 className="text-2xl font-bold">Data Test</h1>

      <div>
        <h2 className="font-bold">Users:</h2>
        <pre>{JSON.stringify(userStats, null, 2)}</pre>
        <p>Total: {adminUsers.length}</p>
      </div>

      <div>
        <h2 className="font-bold">Orders:</h2>
        <pre>{JSON.stringify(orderStats, null, 2)}</pre>
        <p>Total: {adminOrders.length}</p>
      </div>

      <div>
        <h2 className="font-bold">Overview:</h2>
        <pre>{JSON.stringify(analyticsOverview, null, 2)}</pre>
      </div>
    </div>
  );
}