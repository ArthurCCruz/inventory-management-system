import PublicLayout from "@/components/PublicLayout";
import { useAuth } from "@/contexts/AuthContext";
import { Navigate, Outlet } from "react-router-dom";

const PublicRoutes = () => {
  const { isAuthed, isLoading } = useAuth();
  if (isLoading) {
    return null;
  }
  if (isAuthed) {
    return <Navigate to="/dashboard" />;
  }
  return <PublicLayout><Outlet /></PublicLayout>;
};

export default PublicRoutes;