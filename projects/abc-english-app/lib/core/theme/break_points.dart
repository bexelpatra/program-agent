/// Responsive layout breakpoints (dp).
///
/// Kept as plain constants (no Flutter import) so non-UI code can reference
/// them without pulling in material.
class BreakPoints {
  const BreakPoints._();

  /// Below this width → single-pane mobile layout.
  static const double tablet = 600;

  /// At/above this width → 2-pane layout candidate (post-MVP).
  static const double desktop = 1024;
}
