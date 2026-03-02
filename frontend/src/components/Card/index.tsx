import { FC, ReactNode, CSSProperties } from "react";
import { borderRadius, colors, shadows } from "@/styles/theme";

interface CardProps {
  children: ReactNode;
  padding?: 'sm' | 'md' | 'lg';
  hover?: boolean;
  style?: CSSProperties;
  onClick?: () => void;
}

const paddingMap = {
  sm: '1rem',
  md: '1.5rem',
  lg: '2rem',
};

const Card: FC<CardProps> = ({ 
  children, 
  padding = 'lg', 
  hover = false,
  style,
  onClick 
}) => {
  return (
    <div
      onClick={onClick}
      style={{
        background: colors.background.main,
        borderRadius: borderRadius.xl,
        boxShadow: shadows.md,
        border: `1px solid ${colors.border.light}`,
        padding: paddingMap[padding],
        transition: 'all 0.2s ease',
        cursor: onClick ? 'pointer' : 'default',
        ...style,
      }}
      onMouseEnter={(e) => {
        if (hover || onClick) {
          e.currentTarget.style.transform = 'translateY(-2px)';
          e.currentTarget.style.boxShadow = shadows.lg;
        }
      }}
      onMouseLeave={(e) => {
        if (hover || onClick) {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = shadows.md;
        }
      }}
    >
      {children}
    </div>
  );
};

export default Card;
