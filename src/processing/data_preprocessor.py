class DataPreprocessor:
    def __init__(self, normalizers):
        self.normalizers = normalizers

    def preprocess_data(self, vulnerabilities, search_params, source, source_name):
        """Normalize vulnerability data and handle duplicates with improved tracking."""
        normalized = []
        seen_ids = set()
        seen_cves = set()
        duplicates = []
        skipped_vulnerabilities = 0

        param_index = 0  # Index to cycle through search_params

        for vuln in vulnerabilities:
            # Normalize data
            for normalizer in self.normalizers.values():
                norm = normalizer.normalize_data(vuln, source)
                if norm:
                    vuln_id = norm.get('id')
                    if not vuln_id:
                        skipped_vulnerabilities += 1
                        continue
                    cve = norm.get('id')  # Assuming 'id' contains the CVE identifier

                    # Check for duplicates
                    if vuln_id in seen_ids or cve in seen_cves:
                        duplicates.append(norm)
                        continue

                    # Ensure vendor is preserved
                    norm['vendor'] = vuln.get('vendor', 'Unknown')
                    
                    normalized.append(norm)
                    seen_ids.add(vuln_id)
                    seen_cves.add(cve)
                    break

        # Print detailed statistics
        if skipped_vulnerabilities > 0:
            print(f"Total vulnerabilities skipped due to missing ID: {skipped_vulnerabilities}")
        print(f"\nDuplication Statistics for {source_name}:")
        print(f"Total vulnerabilities found for {source_name}: {len(vulnerabilities)}")
        print(f"Unique vulnerabilities for {source_name} after normalization: {len(normalized)}")
        print(f"Duplicates removed for {source_name}: {len(duplicates)}")

        return normalized