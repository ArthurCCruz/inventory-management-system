import { Badge } from "@mantine/core";
import { FC } from "react";
import { colors } from "@/styles/theme";

export type StatusVariant = 'draft' | 'confirmed' | 'done' | 'completed' | 'reserved';

interface StatusBadgeProps {
  status: string;
  variant?: StatusVariant;
}

const StatusBadge: FC<StatusBadgeProps> = ({ status, variant }) => {
  // Auto-detect variant from status string if not provided
  const detectedVariant = variant || detectVariant(status);
  const statusColors = getStatusColors(detectedVariant);

  return (
    <Badge
      style={{
        backgroundColor: statusColors.bg,
        color: statusColors.text,
        border: `1px solid ${statusColors.border}`,
        borderRadius: '9999px',
        padding: '0.25rem 0.75rem',
        fontSize: '0.8rem',
        fontWeight: 500,
        textTransform: 'capitalize',
        transition: 'all 0.2s ease',
      }}
    >
      {status}
    </Badge>
  );
};

// Helper function to detect variant from status string
function detectVariant(status: string): StatusVariant {
  const lowercaseStatus = status.toLowerCase();
  
  if (lowercaseStatus === 'draft') return 'draft';
  if (lowercaseStatus === 'confirmed') return 'confirmed';
  if (lowercaseStatus === 'done' || lowercaseStatus === 'completed') return 'done';
  if (lowercaseStatus === 'reserved') return 'reserved';
  
  return 'draft'; // default
}

// Helper function to get colors based on variant
function getStatusColors(variant: StatusVariant) {
  switch (variant) {
    case 'draft':
      return colors.status.draft;
    case 'confirmed':
      return colors.status.confirmed;
    case 'done':
    case 'completed':
      return colors.status.done;
    case 'reserved':
      return colors.status.reserved;
    default:
      return colors.status.draft;
  }
}

export default StatusBadge;
