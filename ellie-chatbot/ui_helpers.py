"""Small Streamlit UI helpers."""

from __future__ import annotations

import streamlit.components.v1 as components


def stick_to_bottom() -> None:
    """
    Keep the view at the bottom after a full rerun.

    Streamlit resets scroll to the top on rerun; this restores the chat end.
    """
    components.html(
        """
        <script>
        (() => {
          const doc = window.parent.document;
          const scroll = () => {
            const nodes = [
              doc.querySelector('[data-testid="stAppViewContainer"]'),
              doc.querySelector('[data-testid="stMain"]'),
              doc.querySelector('section.main'),
              doc.scrollingElement,
              doc.documentElement,
              doc.body,
            ].filter(Boolean);

            for (const node of nodes) {
              try {
                node.scrollTop = node.scrollHeight;
              } catch (error) {
                // Ignore nodes that are not scrollable.
              }
            }

            try {
              window.parent.scrollTo(0, doc.body.scrollHeight);
            } catch (error) {
              // Ignore cross-frame issues.
            }
          };

          scroll();
          requestAnimationFrame(scroll);
          setTimeout(scroll, 50);
          setTimeout(scroll, 250);
        })();
        </script>
        """,
        height=0,
        width=0,
    )
