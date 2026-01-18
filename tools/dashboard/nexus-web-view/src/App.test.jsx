import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
    it('renders title overlay', () => {
        render(<App />);
        expect(screen.getByText('Nexus 3D')).toBeInTheDocument();
    });
});
