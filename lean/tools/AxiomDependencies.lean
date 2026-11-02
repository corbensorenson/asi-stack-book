import Lean
import AsiStackProofs

open Lean Elab Command

-- Query the elaborated environment, including transitive dependencies and
-- compiler-generated axioms. Source-token scans cannot recover this relation.
run_cmd do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    match info with
    | .thmInfo _ =>
      if let some idx := env.getModuleIdxFor? name then
        let moduleName := env.header.moduleNames[idx.toNat]!
        if moduleName.toString.startsWith "AsiStackProofs" then
          let axioms ← Lean.collectAxioms name
          liftIO <| IO.println <| (Json.mkObj [
            ("declaration", toJson name.toString),
            ("module", toJson moduleName.toString),
            ("axioms", toJson (axioms.map Name.toString))
          ]).compress
    | _ => pure ()
