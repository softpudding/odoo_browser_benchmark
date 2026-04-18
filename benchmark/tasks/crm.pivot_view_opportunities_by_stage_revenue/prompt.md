Go to the **CRM** app and open the **Pipeline**.

Switch the pipeline from its default view to the **Pivot view** by clicking the
pivot icon in the view switcher (top-right of the action, typically the small
grid/matrix icon).

Once in pivot view:

1. **Group rows by Stage.** Click the "+" (Total) row header to open the
   grouping menu, then select **Stage** so rows are grouped by stage.
2. **Set Measures to Expected Revenue.** Click the **Measures** menu button
   and make sure only **Expected Revenue** is selected (uncheck the default
   Count measure if desired; the key requirement is that Expected Revenue
   is checked and visible in the pivot).
3. **Save the current view as a favorite.** Open the **Favorites** menu in
   the search bar, click **Save current search**, enter the name
   exactly `Bench Stage Revenue Pivot`, then click **Save**.

**Rules:**
- The favorite name must be exactly `Bench Stage Revenue Pivot` (case and
  spaces matter).
- The favorite must be saved on the CRM Pipeline (model `crm.lead`).
- The saved pivot context must remember grouping by `stage_id` and the
  `expected_revenue` measure.
- Do not delete or modify any existing opportunities.
