// Force white text on colored Mermaid flowchart backgrounds
document.addEventListener('DOMContentLoaded', function() {
  // Wait for Mermaid to render
  setTimeout(function() {
    // Get all Mermaid diagrams
    const diagrams = document.querySelectorAll('.mermaid svg');

    diagrams.forEach(diagram => {
      // Find all rect elements with colored fills
      const rects = diagram.querySelectorAll('rect');

      rects.forEach(rect => {
        const fill = rect.getAttribute('fill');

        // If it's a dark color, find the parent node and set text to white
        if (fill === '#c41e3a' || fill === '#2d6a2d' || fill === '#d97706' || fill === '#2563eb') {
          const parentNode = rect.closest('g.node');
          if (parentNode) {
            // Set all text elements to white
            const textElements = parentNode.querySelectorAll('p, span, text, tspan');
            textElements.forEach(text => {
              text.style.color = '#fff';
              text.style.fill = '#fff';
            });
          }
        }
      });
    });
  }, 100);
});
